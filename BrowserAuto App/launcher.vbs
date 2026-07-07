' BroserAuto Web - Launcher silencioso (sem janela de terminal)
' Tenta Node.js primeiro, depois Python

Dim shell, fso, nodeFound, pyFound
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

nodeFound = False
pyFound = False

' Verifica se node existe (via where)
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
On Error Resume Next
Dim pyResult
pyResult = shell.Run("cmd /c where python >nul 2>nul", 0, True)
If Err.Number = 0 And pyResult = 0 Then pyFound = True
On Error GoTo 0

If pyFound Then
  shell.Run "python main.py", 0, False
  WScript.Quit 0
End If

' Nada encontrado
MsgBox "BroserAuto Web" & vbCrLf & vbCrLf & _
       "Nenhum runtime encontrado." & vbCrLf & _
       "Instale Node.js (https://nodejs.org) ou Python 3 (https://python.org)", _
       16, "BroserAuto - Erro"
