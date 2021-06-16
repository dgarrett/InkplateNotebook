#include "NoteManager.h"
#include "secrets.h"

String testNote = "---\n"
                  "Note One\n"
                  "Contents\nof\nNote One\n"
                  "---\n"
                  "Note Two\n"
                  "Contents\nof\nNote Two\n";

void NoteManager::DownloadNotes(const String &url)
{
    _display.println("Scanning for WiFi networks...");
    _display.display();

    if (url.length() == 0)
    {
        processNotes(testNote);
        return;
    }

    int n = WiFi.scanNetworks();
    if (n == 0)
    {
        _display.print("No WiFi networks found!");
        _display.partialUpdate();
        while (true)
            ;
    }
    else
    {
        if (n > 10)
            n = 10;
        for (int i = 0; i < n; i++)
        {
            _display.print(WiFi.SSID(i));
            _display.print((WiFi.encryptionType(i) == WIFI_AUTH_OPEN) ? 'O' : '*');
            _display.print('\n');
            _display.print(WiFi.RSSI(i), DEC);
        }
        _display.partialUpdate();
    }

    _display.clearDisplay();
    _display.setCursor(0, 0);
    _display.print("Connecting to ");
    _display.print(ssid);
    WiFi.begin(ssid, pass);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        _display.print('.');
        _display.partialUpdate();
    }
    _display.print("connected");
    _display.partialUpdate();

    HTTPClient http;
    if (http.begin(url))
    {
        if (http.GET() > 0)
        {
            String content(http.getString());
            processNotes(content);
        }
    }
}

String NoteManager::GetCurrentNote()
{
    return _notes.at(_currentNoteName);
}

std::vector<String> NoteManager::AvailableNoteTitles()
{
    std::vector<String> keys;
    for (const auto &note : _notes) {
        keys.push_back(note.first);
    }
    return keys;
}

void NoteManager::processNotes(String raw)
{
    _display.clearDisplay();
    _display.setCursor(0, 0);
    _display.print(raw);
    _display.display();
}