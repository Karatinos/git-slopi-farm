param(
    [int]$Port = 443
)

# Non-secret PRO activation contract. Keep in sync with solve_server.py.
$settings = [pscustomobject]@{
    x_admin_token    = "7a8f9c3e2b1d4056a9c8f7e6d5b4a3c2"
    endpoints        = [pscustomobject]@{ check = "/check"; status = "/status" }
    response_success = [pscustomobject]@{
        valid      = $true
        active     = $true
        exists     = $true
        expires_at = "2099-12-31T23:59:59Z"
        days_left  = 3650
        client     = "CTF"
        plan       = "pro"
    }
}
$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add("https://+:$Port/")
$listener.Start()
Write-Host "Activation server listening on https://0.0.0.0:$Port"
Write-Host "An HTTPS certificate must be bound to this port beforehand (see README_ORGANIZERS.md)."

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $path = $context.Request.Url.AbsolutePath
        if (($context.Request.HttpMethod -eq 'POST' -and $path -eq $settings.endpoints.check) -or
            ($context.Request.HttpMethod -eq 'GET' -and $path -eq $settings.endpoints.status)) {
            Write-Host "$($context.Request.HttpMethod) $path from $($context.Request.RemoteEndPoint)"
            $payload = $settings.response_success | ConvertTo-Json -Compress
            $bytes = [Text.Encoding]::UTF8.GetBytes($payload)
            $context.Response.StatusCode = 200
            $context.Response.ContentType = 'application/json; charset=utf-8'
            $context.Response.Headers.Add('X-Admin-Token', [string]$settings.x_admin_token)
            $context.Response.ContentLength64 = $bytes.Length
            $context.Response.OutputStream.Write($bytes, 0, $bytes.Length)
        } else {
            $context.Response.StatusCode = 404
        }
        $context.Response.Close()
    }
} finally {
    $listener.Close()
}
