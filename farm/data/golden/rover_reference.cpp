// E. Аккуратный подъём — interactive hill climb (C++23).
// State: absolute position + heading; every command (FW/BW/RL/RR) is followed by
// reading the judge's 5 numbers: cur, forward, back, left, right.
// Moves are allowed only when |dh| <= 1. Planning: Dijkstra over (x, y, heading)
// with unit cost per command on the known map; greedy toward the highest reachable
// known cell; explore plateaus/cliffs when no higher cell is reachable; SNP at a
// strict local maximum (the unique peak).
#include <bits/stdc++.h>
using namespace std;

static const int DX[4] = {0, 1, 0, -1};  // 0=N 1=E 2=S 3=W (right turn = +1)
static const int DY[4] = {1, 0, -1, 0};

struct P { int x, y; bool operator<(const P& o) const { return tie(x, y) < tie(o.x, o.y); } };

map<P, long long> H;   // known heights
set<P> visited;        // cells we stood on (all 4 neighbours known)
int X = 0, Y = 0, hd = 0;

bool readView() {
    long long c, f, b, l, r;
    if (!(cin >> c >> f >> b >> l >> r)) return false;
    H[{X, Y}] = c;
    visited.insert({X, Y});
    long long v[4];
    v[hd] = f; v[(hd + 1) % 4] = r; v[(hd + 2) % 4] = b; v[(hd + 3) % 4] = l;
    for (int d = 0; d < 4; ++d) H[{X + DX[d], Y + DY[d]}] = v[d];
    return true;
}

void send(const string& s) { cout << s << endl; }   // endl flushes

int main() {
    ios::sync_with_stdio(false);
    if (!readView()) return 0;
    for (;;) {
        long long cur = H[{X, Y}];
        // strict local maximum => peak
        bool peak = true;
        for (int d = 0; d < 4; ++d)
            if (H[{X + DX[d], Y + DY[d]}] >= cur) { peak = false; break; }
        if (peak) { send("SNP"); return 0; }

        // Dijkstra over (cell, heading) through known cells, legal steps only.
        // Only visited cells may be expanded (their neighbours are known);
        // unvisited known cells are valid endpoints.
        using S = tuple<int, int, int>;
        map<S, int> dist; map<S, pair<S, string>> par;
        priority_queue<pair<int, S>, vector<pair<int, S>>, greater<>> pq;
        S st{X, Y, hd}; dist[st] = 0; pq.push({0, st});
        while (!pq.empty()) {
            auto [dd, s] = pq.top(); pq.pop();
            if (dist[s] != dd) continue;
            auto [x, y, h] = s;
            if (!visited.count({x, y})) continue;   // cannot see further from here
            auto relax = [&](S t, const string& cmd) {
                if (!dist.count(t) || dist[t] > dd + 1) { dist[t] = dd + 1; par[t] = {s, cmd}; pq.push({dd + 1, t}); }
            };
            relax({x, y, (h + 3) % 4}, "RL");
            relax({x, y, (h + 1) % 4}, "RR");
            for (int k : {0, 2}) {                   // FW / BW
                int d = (h + k) % 4;
                P n{x + DX[d], y + DY[d]};
                if (!H.count(n)) continue;
                if (llabs(H[n] - H[{x, y}]) > 1) continue;
                relax({n.x, n.y, h}, k == 0 ? "FW" : "BW");
            }
        }
        // best cell by cost for each reachable cell
        map<P, pair<int, S>> best;
        for (auto& [s, d] : dist) {
            P p{get<0>(s), get<1>(s)};
            if (!best.count(p) || best[p].first > d) best[p] = {d, s};
        }
        // Best-first frontier search. Visited cells are fully known, so the goal
        // is always the highest UNVISITED reachable cell (cheapest on ties):
        // on a smooth slope that is simply the uphill neighbour (optimal), and
        // around a +2 cliff it walks the frontier instead of bouncing between
        // known dead ends. Every goal becomes visited once reached => no loops.
        // (The peak is recognised only on a visited cell — handled above.)
        optional<P> goal; optional<pair<long long, int>> key;
        for (auto& [p, v] : best) {
            if (visited.count(p)) continue;
            pair<long long, int> k{H[p], -v.first};
            if (!key || k > *key) { key = k; goal = p; }
        }
        if (!goal) { send("SNP"); return 0; }        // nothing left to explore
        S target = best[*goal].second;

        // first command of the path to target
        S s = target; string cmd;
        while (par.count(s) && par[s].first != st) s = par[s].first;
        cmd = par[s].second;
        send(cmd);
        if (cmd == "RL") hd = (hd + 3) % 4;
        else if (cmd == "RR") hd = (hd + 1) % 4;
        else { int d = cmd == "FW" ? hd : (hd + 2) % 4; X += DX[d]; Y += DY[d]; }
        if (!readView()) return 0;
    }
}
