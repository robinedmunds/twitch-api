#
# Robin's start streamlink script
# new-item -path .\lirik.ps1 -ItemType HardLink -value .\_twitch.ps1



Write-Output("


  _______       _ _       _      _
 |__   __|     (_) |     | |    | |
    | |_      ___| |_ ___| |__  | |___   __
    | \ \ /\ / / | __/ __| '_ \ | __\ \ / /
    | |\ V  V /| | || (__| | | || |_ \ V /
    |_| \_/\_/ |_|\__\___|_| |_(_)__| \_/



")
$streamer = Read-Host -Prompt "Enter twitch name"
Write-Output("> Attemping to view " + $streamer + " on twitch.tv ...
")
streamlink twitch.tv/$streamer best