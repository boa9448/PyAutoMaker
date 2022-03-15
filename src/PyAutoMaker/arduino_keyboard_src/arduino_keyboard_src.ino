#include "Keyboard.h"
#include "Mouse.h"

//디버깅용 출력이 필요하다면 주석해제
//#define DEBUG_MODE

#define VERSION_MAJOR 0
#define VERSION_MINOR 1
#define VERSION_PATCH 0

#define OPCODE_FIRMWARE_INFO_DATA 1
#define OPCODE_KEY_DATA 2
#define OPCODE_MOUSE_BUTTON_DATA 3
#define OPCODE_MOUSE_MOVE_DATA 4

#define ARDUINO_KEY_PRESS 1
#define ARDUINO_KEY_RELEASE 2

#define ARDUINO_BUTTON_LEFT 1
#define ARDUINO_BUTTON_RIGHT 2
#define ARDUINO_BUTTON_MIDDLE 4

#define ARDUINO_BUTTON_STATUS_PRESS 1
#define ARDUINO_BUTTON_STATUS_RELEASE 2

#pragma pack(push, 1)

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

struct FirmwareInfoData
{
    char major;
    char minor;
    char patch;
};

union ArduinoData
{
    struct KeyData key_data;
    struct MouseButtonData mouse_button_data;
    struct MouseMoveData mouse_move_data;
    struct FirmwareInfoData firmware_info_data;
};

struct ArduinoPacket
{
    char opcode;
    union ArduinoData data;
};

#pragma pack(pop)


struct ArduinoPacket g_packet;

void setup()
{
    Serial.begin(115200);
    while(!Serial)
    {
      ;
    }
    Keyboard.begin();
    Mouse.begin();
}

void loop()
{
    if(Serial.available() >= sizeof(g_packet))
    {
        Serial.readBytes((char*)&g_packet, sizeof(g_packet));

        if(g_packet.opcode == OPCODE_KEY_DATA)
        {
            if(g_packet.data.key_data.key_status == ARDUINO_KEY_PRESS)
                Keyboard.press(g_packet.data.key_data.key_code);
            else if(g_packet.data.key_data.key_status  == ARDUINO_KEY_RELEASE)
                Keyboard.release(g_packet.data.key_data.key_code);
            
        #ifdef DEBUG_MODE
            //sprintf(szTemp, "key_code : %d, key_status : %d", recvKeyData.key_code, recvKeyData.key_status);
            //Serial.write(strlen(szTemp));
            //Serial.print(szTemp);
            //Serial.println();
        #endif
        }
        else if(g_packet.opcode == OPCODE_MOUSE_BUTTON_DATA)
        {
            if(g_packet.data.mouse_button_data.button_status == ARDUINO_BUTTON_STATUS_PRESS)
                Mouse.press(g_packet.data.mouse_button_data.button_code);
            else if(g_packet.data.mouse_button_data.button_status == ARDUINO_BUTTON_STATUS_RELEASE)
                Mouse.release(g_packet.data.mouse_button_data.button_code);
            
        #ifdef DEBUG_MODE
            //sprintf(szTemp, "button_code : %d, button_status : %d", recvMouseButtonData.button_code, recvMouseButtonData.button_status);
            //Serial.write(strlen(szTemp));
            //Serial.print(szTemp);
            //Serial.println();
        #endif
        }
        else if(g_packet.opcode == OPCODE_MOUSE_MOVE_DATA)
        {
            Mouse.move(g_packet.data.mouse_move_data.x, g_packet.data.mouse_move_data.y, 0);
            //Mouse.move(100, 100, 0);
            
        #ifdef DEBUG_MODE
            sprintf(szTemp, "arduino recv x : %d, y : %d", recvMouseMoveData.x, recvMouseMoveData.y);
            //Serial.write(strlen(szTemp));
            //Serial.print(szTemp);
            //Serial.println();
        #endif
        }
        else if(g_packet.opcode == OPCODE_FIRMWARE_INFO_DATA)
        {
            g_packet.opcode = OPCODE_FIRMWARE_INFO_DATA;
            g_packet.data.firmware_info_data = {VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH};
        
            Serial.write((char*)&g_packet, sizeof(g_packet));
        }
    }
}
