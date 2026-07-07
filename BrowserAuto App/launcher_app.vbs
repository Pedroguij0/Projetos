Dim shell, fso, nodeFound, pyFound
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

nodeFound = False
pyFound = False

' Primeiro tenta Node.js (mais rapido)
Dim nodeResult
On Error Resume Next
nodeResult = shell.Run("cmd /c where node >nul 2>nul", 0, True)
If Err.Number = 0 And nodeResult = 0 Then nodeFound = True
On Error GoTo 0

If nodeFound Then
  shell.Run "node server.js", 0, False
  WScript.Quit 0
End If

' Fallback: Python
Dim pyResult
On Error Resume Next
pyResult = shell.Run("cmd /c python --version >nul 2>nul", 0, True)
If Err.Number = 0 And pyResult = 0 Then pyFound = True
On Error GoTo 0

If pyFound Then
  shell.Run "python main.py", 0, False
  WScript.Quit 0
End If

MsgBox "BroserAuto Web" & vbCrLf & vbCrLf & _
       "Nenhum runtime encontrado." & vbCrLf & _
       "Instale Node.js (https://nodejs.org) ou Python 3 (https://python.org)", _
       16, "BroserAuto - Erro"
