function DoReq($name, $method, $url, $body=$null) {
    Write-Output "=== $name ==="
    try {
        if ($body -ne $null) {
            $json = $body | ConvertTo-Json -Depth 10
            $r = Invoke-RestMethod -Uri $url -Method $method -ContentType 'application/json' -Body $json
            Write-Output "Status: 200"
            $r | ConvertTo-Json -Depth 10
        } else {
            $r = Invoke-RestMethod -Uri $url -Method $method
            Write-Output "Status: 200"
            $r | ConvertTo-Json -Depth 10
        }
    } catch {
        $err = $_.Exception
        if ($err.Response -ne $null) {
            $resp = $err.Response
            $status = $resp.StatusCode.Value__
            $reader = New-Object System.IO.StreamReader($resp.GetResponseStream())
            $bodytext = $reader.ReadToEnd()
            Write-Output ("Status: " + $status)
            Write-Output $bodytext
        } else {
            Write-Output ("Error: " + $_.Exception.Message)
        }
    }
}

$base = 'https://stage1-string-analyzer.onrender.com'

DoReq 'POST create racecar (no slash)' 'POST' ($base + '/strings') @{value='racecar'}
DoReq 'POST duplicate racecar' 'POST' ($base + '/strings') @{value='racecar'}
DoReq 'POST invalid type' 'POST' ($base + '/strings') @{value=123}
DoReq 'GET item' 'GET' ($base + '/strings/racecar')
DoReq 'GET filter is_palindrome' 'GET' ($base + '/strings?is_palindrome=true')
DoReq 'GET NLP palindromic strings' 'GET' ($base + '/strings/filter-by-natural-language?query=palindromic+strings')
DoReq 'DELETE item' 'DELETE' ($base + '/strings/racecar')
DoReq 'GET after delete' 'GET' ($base + '/strings/racecar')
