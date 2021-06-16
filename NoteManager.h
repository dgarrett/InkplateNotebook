#pragma once

#include <Inkplate.h>
#include <vector>
#include <map>

class NoteManager {
public:
    NoteManager(Inkplate &display) : _display(display), _currentNoteName() {}
    void DownloadNotes(const String &url);
    String GetCurrentNote();
    std::vector<String> AvailableNoteTitles();

private:
    Inkplate &_display;
    void processNotes(String raw);
    std::map<String, String> _notes;
    String _currentNoteName;
};