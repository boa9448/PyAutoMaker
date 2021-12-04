#include "Keyboard.h"
#include "Mouse.h"

//디버깅용 출력이 필요하다면 주석해제
#define DEBUG_MODE

#define CMD_START_SIGN '#'
#define CMD_OPCODE_KEY_DATA 1
#define CMD_OPCODE_MOUSE_BUTTON 2
#define CMD_OPCODE_MOUSE_MOVE 3

#define KEY_PRESS 1
#define KEY_RELEASE 2

#define BUTTON_LEFT 1
#define BUTTON_RIGHT 2
#define BUTTON_MIDDLE 4

#define BUTTON_STATUS_PRESS 1
#define BUTTON_STATUS_RELEASE 2

#pragma pack(push, 1)
struct CmdHeader
{
    unsigned char start_sign;
    uint16_t opcode;
};

struct KeyData
{
    unsigned char key_code;
    unsigned char key_status;
};

struct MouseButtonData
{
    unsigned char button_code;
    unsigned char button_status;
};

struct MouseMoveData
{
    char x;
    char y;
};
#pragma pack(pop)


CmdHeader header = {0, };
KeyData recvKeyData = {0, };
MouseButtonData recvMouseButtonData = {0, };
MouseMoveData recvMouseMoveData = {0, };
char szTemp[255] = {0, };

void ClearSerialBuffer()
{
    while(Serial.available())
    {
        if(Serial.peek() != CMD_START_SIGN)
            Serial.read();
    }
}

void setup()
{
    Serial.begin(9600);
    Keyboard.begin();
    Mouse.begin();
}

void loop()
{
    if(Serial.available())
    {
        Serial.readBytes((char*)&header, sizeof(header));
        if(header.start_sign != CMD_START_SIGN)
        {
            ClearSerialBuffer();
            return;
        }

        if(header.opcode == CMD_OPCODE_KEY_DATA)
        {
            Serial.readBytes((char*)&recvKeyData, sizeof(recvKeyData));
            if(recvKeyData.key_status == KEY_PRESS) Keyboard.press(recvKeyData.key_code);
            else if(recvKeyData.key_status == KEY_RELEASE) Keyboard.release(recvKeyData.key_code);
            
        #ifdef DEBUG_MODE
            sprintf(szTemp, "key_code : %d, key_status : %d", recvKeyData.key_code, recvKeyData.key_status);
            Serial.println(szTemp);
        #endif
        }
        else if(header.opcode == CMD_OPCODE_MOUSE_BUTTON)
        {
            Serial.readBytes((char*)&recvMouseButtonData, sizeof(recvMouseButtonData));
            if(recvMouseButtonData.button_status == BUTTON_STATUS_PRESS) Mouse.press(recvMouseButtonData.button_code);
            else if(recvMouseButtonData.button_status == BUTTON_STATUS_RELEASE) Mouse.release(recvMouseButtonData.button_code);
            
        #ifdef DEBUG_MODE
            sprintf(szTemp, "button_code : %d, button_status : %d", recvMouseButtonData.button_code, recvMouseButtonData.button_status);
            Serial.println(szTemp);
        #endif
        }
        else if(header.opcode == CMD_OPCODE_MOUSE_MOVE)
        {
            Serial.readBytes((char*)&recvMouseMoveData, sizeof(recvMouseMoveData));
            Mouse.move(recvMouseMoveData.x, recvMouseMoveData.y, 0);
            
        #ifdef DEBUG_MODE
            sprintf(szTemp, "x : %d, y : %d", recvMouseMoveData.x, recvMouseMoveData.y);
            Serial.println(szTemp);
        #endif
        }
    }
}
