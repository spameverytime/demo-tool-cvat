/**
 * Mouse Helper - Windows Portable Native Application (Win32 API)
 * Hoạt động độc lập, không cần cài đặt (Single-File Portable Executable).
 * Khoá cứng trục di chuyển chuột phần cứng (X hoặc Y) khi giữ phím Shift.
 */

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// ID các control giao diện
#define ID_CHECK_ENABLE   101
#define ID_RADIO_X        102
#define ID_RADIO_Y        103
#define ID_RADIO_AUTO     104
#define ID_RADIO_SHIFT    105
#define ID_RADIO_ALT      106
#define ID_RADIO_CTRL     107
#define ID_BTN_MINIMIZE   108
#define ID_BTN_EXIT       109
#define ID_TIMER_UPDATE   110

// Biến trạng thái toàn cục
static bool g_enabled = true;
static char g_axis_mode = 'X';      // 'X', 'Y', 'A' (Auto)
static int  g_modifier_vk = VK_SHIFT; // VK_SHIFT, VK_MENU (Alt), VK_CONTROL
static bool g_is_locked = false;
static bool g_key_pressed = false;
static int  g_anchor_x = 0;
static int  g_anchor_y = 0;
static int  g_current_x = 0;
static int  g_current_y = 0;
static char g_auto_axis = 0;
static HANDLE g_thread = NULL;
static bool g_running = true;

// Handle các widget
static HWND hCheckEnable;
static HWND hRadioX, hRadioY, hRadioAuto;
static HWND hRadioShift, hRadioAlt, hRadioCtrl;
static HWND hLblPos, hLblKey, hLblLock;

// Vòng lặp luồng chạy ngầm khoá cứng toạ độ chuột ở tần số cao (~200Hz)
DWORD WINAPI MouseClampThread(LPVOID lpParam) {
    while (g_running) {
        if (!g_enabled) {
            Sleep(50);
            continue;
        }

        SHORT keyState = GetAsyncKeyState(g_modifier_vk);
        bool isDown = (keyState & 0x8000) != 0;
        g_key_pressed = isDown;

        POINT pt;
        GetCursorPos(&pt);
        g_current_x = pt.x;
        g_current_y = pt.y;

        if (isDown) {
            if (!g_is_locked) {
                // Điểm bắt đầu giữ Shift: Chốt toạ độ neo gốc
                g_anchor_x = pt.x;
                g_anchor_y = pt.y;
                g_is_locked = true;
                g_auto_axis = 0;
            }

            char effective_axis = g_axis_mode;
            if (g_axis_mode == 'A') {
                if (g_auto_axis == 0) {
                    int dx = abs(pt.x - g_anchor_x);
                    int dy = abs(pt.y - g_anchor_y);
                    if (dx >= 6 || dy >= 6) {
                        g_auto_axis = (dx >= dy) ? 'X' : 'Y';
                    }
                }
                effective_axis = g_auto_axis ? g_auto_axis : 'X';
            }

            if (effective_axis == 'X') {
                // KHOÁ TRỤC X: Giữ nguyên Y tại g_anchor_y, cho phép X tự do
                if (pt.y != g_anchor_y) {
                    SetCursorPos(pt.x, g_anchor_y);
                    g_current_y = g_anchor_y;
                }
            } else if (effective_axis == 'Y') {
                // KHOÁ TRỤC Y: Giữ nguyên X tại g_anchor_x, cho phép Y tự do
                if (pt.x != g_anchor_x) {
                    SetCursorPos(g_anchor_x, pt.y);
                    g_current_x = g_anchor_x;
                }
            }

            Sleep(5); // 200 Hz
        } else {
            if (g_is_locked) {
                g_is_locked = false;
                g_auto_axis = 0;
            }
            Sleep(15);
        }
    }
    return 0;
}

// Xử lý sự kiện cửa sổ Win32
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
        case WM_CREATE: {
            HFONT hFont = CreateFontW(14, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE,
                                      DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
                                      CLEARTYPE_QUALITY, DEFAULT_PITCH | FF_DONTCARE, L"Segoe UI");

            HFONT hFontBold = CreateFontW(14, 0, 0, 0, FW_BOLD, FALSE, FALSE, FALSE,
                                          DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
                                          CLEARTYPE_QUALITY, DEFAULT_PITCH | FF_DONTCARE, L"Segoe UI");

            // Checkbox Bật/Tắt
            hCheckEnable = CreateWindowW(L"BUTTON", L"Kích hoạt Mouse Helper (Bật / Tắt)",
                                         WS_VISIBLE | WS_CHILD | BS_AUTOCHECKBOX,
                                         20, 15, 300, 24, hwnd, (HMENU)ID_CHECK_ENABLE, NULL, NULL);
            SendMessage(hCheckEnable, BM_SETCHECK, BST_CHECKED, 0);
            SendMessage(hCheckEnable, WM_SETFONT, (WPARAM)hFontBold, TRUE);

            // Group 1: Phương khoá trục
            CreateWindowW(L"BUTTON", L"Phương khoá trục (khi giữ phím)",
                          WS_VISIBLE | WS_CHILD | BS_GROUPBOX,
                          20, 50, 440, 110, hwnd, NULL, NULL, NULL);

            hRadioX = CreateWindowW(L"BUTTON", L"Trục X (Chỉ di chuyển ngang)",
                                    WS_VISIBLE | WS_CHILD | BS_AUTORADIOBUTTON | WS_GROUP,
                                    35, 75, 260, 22, hwnd, (HMENU)ID_RADIO_X, NULL, NULL);
            hRadioY = CreateWindowW(L"BUTTON", L"Trục Y (Chỉ di chuyển dọc)",
                                    WS_VISIBLE | WS_CHILD | BS_AUTORADIOBUTTON,
                                    35, 100, 260, 22, hwnd, (HMENU)ID_RADIO_Y, NULL, NULL);
            hRadioAuto = CreateWindowW(L"BUTTON", L"Tự động (Theo hướng di chuyển ban đầu)",
                                       WS_VISIBLE | WS_CHILD | BS_AUTORADIOBUTTON,
                                       35, 125, 320, 22, hwnd, (HMENU)ID_RADIO_AUTO, NULL, NULL);
            SendMessage(hRadioX, BM_SETCHECK, BST_CHECKED, 0);
            SendMessage(hRadioX, WM_SETFONT, (WPARAM)hFont, TRUE);
            SendMessage(hRadioY, WM_SETFONT, (WPARAM)hFont, TRUE);
            SendMessage(hRadioAuto, WM_SETFONT, (WPARAM)hFont, TRUE);

            // Group 2: Phím kích hoạt
            CreateWindowW(L"BUTTON", L"Phím kích hoạt (Nhấn giữ khi vẽ)",
                          WS_VISIBLE | WS_CHILD | BS_GROUPBOX,
                          20, 170, 440, 90, hwnd, NULL, NULL, NULL);

            hRadioShift = CreateWindowW(L"BUTTON", L"Phím Shift (Mặc định)",
                                        WS_VISIBLE | WS_CHILD | BS_AUTORADIOBUTTON | WS_GROUP,
                                        35, 195, 200, 22, hwnd, (HMENU)ID_RADIO_SHIFT, NULL, NULL);
            hRadioAlt = CreateWindowW(L"BUTTON", L"Phím Alt",
                                      WS_VISIBLE | WS_CHILD | BS_AUTORADIOBUTTON,
                                      35, 225, 100, 22, hwnd, (HMENU)ID_RADIO_ALT, NULL, NULL);
            hRadioCtrl = CreateWindowW(L"BUTTON", L"Phím Ctrl",
                                       WS_VISIBLE | WS_CHILD | BS_AUTORADIOBUTTON,
                                       150, 225, 100, 22, hwnd, (HMENU)ID_RADIO_CTRL, NULL, NULL);
            SendMessage(hRadioShift, BM_SETCHECK, BST_CHECKED, 0);
            SendMessage(hRadioShift, WM_SETFONT, (WPARAM)hFont, TRUE);
            SendMessage(hRadioAlt, WM_SETFONT, (WPARAM)hFont, TRUE);
            SendMessage(hRadioCtrl, WM_SETFONT, (WPARAM)hFont, TRUE);

            // Group 3: Thông số thời gian thực
            CreateWindowW(L"BUTTON", L"Thông số chuột thời gian thực",
                          WS_VISIBLE | WS_CHILD | BS_GROUPBOX,
                          20, 270, 440, 95, hwnd, NULL, NULL, NULL);

            hLblPos = CreateWindowW(L"STATIC", L"Toạ độ: X = 0, Y = 0",
                                    WS_VISIBLE | WS_CHILD,
                                    35, 295, 400, 18, hwnd, NULL, NULL, NULL);
            hLblKey = CreateWindowW(L"STATIC", L"Phím kích hoạt: Đang thả (Tự do)",
                                    WS_VISIBLE | WS_CHILD,
                                    35, 315, 400, 18, hwnd, NULL, NULL, NULL);
            hLblLock = CreateWindowW(L"STATIC", L"Trạng thái khoá: TỰ DO (2 chiều)",
                                     WS_VISIBLE | WS_CHILD,
                                     35, 335, 400, 18, hwnd, NULL, NULL, NULL);
            SendMessage(hLblPos, WM_SETFONT, (WPARAM)hFont, TRUE);
            SendMessage(hLblKey, WM_SETFONT, (WPARAM)hFont, TRUE);
            SendMessage(hLblLock, WM_SETFONT, (WPARAM)hFontBold, TRUE);

            // Hướng dẫn
            HWND hHint = CreateWindowW(L"STATIC",
                                       L"💡 Hướng dẫn: Mở Chrome/CVAT hoặc bất kỳ phần mềm nào, nhấn giữ Shift để vẽ đường thẳng ngang hoặc dọc tuyệt đối!",
                                       WS_VISIBLE | WS_CHILD,
                                       20, 375, 440, 36, hwnd, NULL, NULL, NULL);
            SendMessage(hHint, WM_SETFONT, (WPARAM)hFont, TRUE);

            // Nút bấm
            HWND hBtnExit = CreateWindowW(L"BUTTON", L"Đóng ứng dụng",
                                          WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
                                          350, 420, 110, 30, hwnd, (HMENU)ID_BTN_EXIT, NULL, NULL);
            SendMessage(hBtnExit, WM_SETFONT, (WPARAM)hFont, TRUE);

            // Đăng ký phím tắt toàn cục
            RegisterHotKey(hwnd, 1, MOD_ALT | MOD_SHIFT, 'S'); // Alt+Shift+S: Bật/Tắt
            RegisterHotKey(hwnd, 2, MOD_ALT | MOD_SHIFT, 'X'); // Alt+Shift+X: Trục X
            RegisterHotKey(hwnd, 3, MOD_ALT | MOD_SHIFT, 'Y'); // Alt+Shift+Y: Trục Y
            RegisterHotKey(hwnd, 4, MOD_ALT | MOD_SHIFT, 'A'); // Alt+Shift+A: Auto

            // Timer cập nhật UI 20Hz
            SetTimer(hwnd, ID_TIMER_UPDATE, 50, NULL);
            break;
        }

        case WM_COMMAND: {
            int id = LOWORD(wParam);
            if (id == ID_CHECK_ENABLE) {
                g_enabled = (SendMessage(hCheckEnable, BM_GETCHECK, 0, 0) == BST_CHECKED);
            } else if (id == ID_RADIO_X) {
                g_axis_mode = 'X';
            } else if (id == ID_RADIO_Y) {
                g_axis_mode = 'Y';
            } else if (id == ID_RADIO_AUTO) {
                g_axis_mode = 'A';
            } else if (id == ID_RADIO_SHIFT) {
                g_modifier_vk = VK_SHIFT;
            } else if (id == ID_RADIO_ALT) {
                g_modifier_vk = VK_MENU;
            } else if (id == ID_RADIO_CTRL) {
                g_modifier_vk = VK_CONTROL;
            } else if (id == ID_BTN_EXIT) {
                PostQuitMessage(0);
            }
            break;
        }

        case WM_HOTKEY: {
            int id = (int)wParam;
            if (id == 1) {
                g_enabled = !g_enabled;
                SendMessage(hCheckEnable, BM_SETCHECK, g_enabled ? BST_CHECKED : BST_UNCHECKED, 0);
            } else if (id == 2) {
                g_axis_mode = 'X';
                SendMessage(hRadioX, BM_SETCHECK, BST_CHECKED, 0);
                SendMessage(hRadioY, BM_SETCHECK, BST_UNCHECKED, 0);
                SendMessage(hRadioAuto, BM_SETCHECK, BST_UNCHECKED, 0);
            } else if (id == 3) {
                g_axis_mode = 'Y';
                SendMessage(hRadioX, BM_SETCHECK, BST_UNCHECKED, 0);
                SendMessage(hRadioY, BM_SETCHECK, BST_CHECKED, 0);
                SendMessage(hRadioAuto, BM_SETCHECK, BST_UNCHECKED, 0);
            } else if (id == 4) {
                g_axis_mode = 'A';
                SendMessage(hRadioX, BM_SETCHECK, BST_UNCHECKED, 0);
                SendMessage(hRadioY, BM_SETCHECK, BST_UNCHECKED, 0);
                SendMessage(hRadioAuto, BM_SETCHECK, BST_CHECKED, 0);
            }
            break;
        }

        case WM_TIMER: {
            if (wParam == ID_TIMER_UPDATE) {
                wchar_t bufPos[64];
                swprintf(bufPos, 64, L"Toạ độ: X = %d, Y = %d", g_current_x, g_current_y);
                SetWindowTextW(hLblPos, bufPos);

                if (g_key_pressed) {
                    SetWindowTextW(hLblKey, L"Phím kích hoạt: ĐANG GIỮ (KHOÁ TRỤC ON)");
                } else {
                    SetWindowTextW(hLblKey, L"Phím kích hoạt: Đang thả (Tự do)");
                }

                if (g_is_locked && g_enabled) {
                    wchar_t bufLock[64];
                    char ax = g_axis_mode;
                    if (ax == 'A') ax = g_auto_axis ? g_auto_axis : 'X';
                    swprintf(bufLock, 64, L"Trạng thái khoá: 🔒 ĐANG KHOÁ TRỤC %C", ax);
                    SetWindowTextW(hLblLock, bufLock);
                } else {
                    SetWindowTextW(hLblLock, L"Trạng thái khoá: TỰ DO (2 chiều)");
                }
            }
            break;
        }

        case WM_DESTROY: {
            g_running = false;
            KillTimer(hwnd, ID_TIMER_UPDATE);
            UnregisterHotKey(hwnd, 1);
            UnregisterHotKey(hwnd, 2);
            UnregisterHotKey(hwnd, 3);
            UnregisterHotKey(hwnd, 4);
            PostQuitMessage(0);
            break;
        }

        default:
            return DefWindowProcW(hwnd, msg, wParam, lParam);
    }
    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // Khởi động luồng khoá chuột chạy nền
    g_thread = CreateThread(NULL, 0, MouseClampThread, NULL, 0, NULL);

    WNDCLASSEXW wc = {0};
    wc.cbSize = sizeof(WNDCLASSEXW);
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_BTNFACE + 1);
    wc.lpszClassName = L"MouseHelperClass";

    if (!RegisterClassExW(&wc)) {
        return 1;
    }

    HWND hwnd = CreateWindowExW(
        WS_EX_DLGMODALFRAME,
        L"MouseHelperClass",
        L"Mouse Helper - Ortho Axis Lock (Windows Portable)",
        WS_VISIBLE | WS_SYSMENU | WS_MINIMIZEBOX,
        CW_USEDEFAULT, CW_USEDEFAULT,
        495, 500,
        NULL, NULL, hInstance, NULL
    );

    if (!hwnd) {
        return 1;
    }

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    MSG msg;
    while (GetMessageW(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessageW(&msg);
    }

    g_running = false;
    if (g_thread) {
        WaitForSingleObject(g_thread, 500);
        CloseHandle(g_thread);
    }

    return (int)msg.wParam;
}
