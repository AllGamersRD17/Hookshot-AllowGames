/* (Allow Games) Discord Rich Presence: while the game runs, a player's Discord profile says "Playing Hookshot - Allow Games
   Edition", with the time played and a button to this edition's download page. It talks to the Discord app on the same PC through
   its local IPC pipe (\\.\pipe\discord-ipc-0 .. 9): no Discord SDK, no network, nothing sent anywhere but the player's own Discord.
   Nothing happens when Discord is not running, and the game never waits for it (its own thread, a retry every 15 s).

   It needs the Allow Games application's id from the Discord Developer Portal (AG_DISCORD_CLIENT_ID below, or
   ALLOWGAMES_DISCORD_ID in hookshot_env.txt). ALLOWGAMES_DISCORD=0 in hookshot_env.txt, or the Insert menu's Discord row
   (Gameplay tab, option 65: HOS_OPT_AG_DISCORD), turns it off. Windows only; elsewhere it does nothing. */
#include "hos.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* The Discord application of Allow Games (its name is what Discord shows after "Playing"). Empty: off until it is set */
#ifndef AG_DISCORD_CLIENT_ID
#define AG_DISCORD_CLIENT_ID ""
#endif
#define AG_DISCORD_URL "https://github.com/AllGamersRD17/Hookshot-AllowGames/releases/latest"

#ifdef _WIN32
#include <windows.h>

int rx_option(int id, int otherwise);

static const char *client_id(void) {
    const char *e = getenv("ALLOWGAMES_DISCORD_ID");
    return e && *e ? e : AG_DISCORD_CLIENT_ID;
}

/* One frame of Discord's IPC: op, length (both little-endian 32 bits), then the JSON */
static int send_frame(HANDLE pipe, uint32_t op, const char *json) {
    const uint32_t len = (uint32_t)strlen(json);
    char head[8];
    memcpy(head, &op, 4);
    memcpy(head + 4, &len, 4);
    DWORD n = 0;
    if (!WriteFile(pipe, head, 8, &n, NULL) || n != 8) return 0;
    if (!WriteFile(pipe, json, len, &n, NULL) || n != len) return 0;
    return 1;
}

/* A frame's answer read and dropped (its op returned; -1 when the pipe is gone) */
static int read_frame(HANDLE pipe) {
    char head[8];
    DWORD n = 0;
    if (!ReadFile(pipe, head, 8, &n, NULL) || n != 8) return -1;
    uint32_t op, len;
    memcpy(&op, head, 4);
    memcpy(&len, head + 4, 4);
    char buf[512];
    while (len) {
        const DWORD want = len < sizeof buf ? len : (DWORD)sizeof buf;
        if (!ReadFile(pipe, buf, want, &n, NULL) || !n) return -1;
        len -= n;
    }
    return (int)op;
}

static HANDLE open_pipe(void) {
    for (int i = 0; i < 10; i++) {
        char name[64];
        snprintf(name, sizeof name, "\\\\.\\pipe\\discord-ipc-%d", i);
        HANDLE h = CreateFileA(name, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
        if (h != INVALID_HANDLE_VALUE) return h;
    }
    return INVALID_HANDLE_VALUE;
}

static int set_activity(HANDLE pipe, long long started, int on) {
    static unsigned nonce;
    char json[1024];
    if (!on)
        snprintf(json, sizeof json, "{\"cmd\":\"SET_ACTIVITY\",\"args\":{\"pid\":%lu},\"nonce\":\"ag%u\"}",
                 (unsigned long)GetCurrentProcessId(), ++nonce);
    else
        snprintf(json, sizeof json,
                 "{\"cmd\":\"SET_ACTIVITY\",\"args\":{\"pid\":%lu,\"activity\":{"
                 "\"details\":\"The Legend of Zelda: Ocarina of Time\","
                 "\"state\":\"Hookshot - Allow Games Edition\","
                 "\"timestamps\":{\"start\":%lld},"
                 "\"assets\":{\"large_image\":\"allowgames\",\"large_text\":\"Allow Games Edition\"},"
                 "\"buttons\":[{\"label\":\"Descargar / Download\",\"url\":\"" AG_DISCORD_URL "\"}]"
                 "}},\"nonce\":\"ag%u\"}",
                 (unsigned long)GetCurrentProcessId(), started, ++nonce);
    if (!send_frame(pipe, 1, json)) return 0;
    return read_frame(pipe) >= 0;
}

static DWORD WINAPI discord_thread(LPVOID unused) {
    (void)unused;
    const long long started = (long long)time(NULL);
    int logged = 0;
    for (;;) {
        HANDLE pipe = open_pipe();
        if (pipe != INVALID_HANDLE_VALUE) {
            char hello[160];
            snprintf(hello, sizeof hello, "{\"v\":1,\"client_id\":\"%s\"}", client_id());
            int shown = -1;
            if (send_frame(pipe, 0, hello) && read_frame(pipe) >= 0) {
                if (!logged++) hos_log("discord: connected, the Allow Games presence is shown");
                for (;;) {   /* (the menu's Discord row followed, every 2 s) */
                    const int on = rx_option(65, 1) != 0;
                    if (on != shown) {
                        if (!set_activity(pipe, started, on)) break;
                        shown = on;
                    }
                    Sleep(2000);
                }
            }
            CloseHandle(pipe);
        }
        Sleep(15000);   /* (Discord not running, or closed: tried again later) */
    }
    return 0;
}

void ag_discord_start(void) {
    const char *off = getenv("ALLOWGAMES_DISCORD");
    if (off && !strcmp(off, "0")) return;
    if (!client_id()[0]) {
        hos_log("discord: no application id (AG_DISCORD_CLIENT_ID, ALLOWGAMES_DISCORD_ID): the presence is off");
        return;
    }
    HANDLE t = CreateThread(NULL, 64 * 1024, discord_thread, NULL, 0, NULL);
    if (t) CloseHandle(t);
}
#else
void ag_discord_start(void) {}
#endif
