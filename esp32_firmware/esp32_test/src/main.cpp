#include <Arduino.h>
#include <ESP32Servo.h>

const int SWITCH_PIN = 27;
const int SERVO_PIN = 18;

const int HOME_POS = 0;
const int FEED_POS = 90;

const unsigned long DEBOUNCE_MS = 100;
const unsigned long check_time = 7000;

int feed_attempt = 0;

Servo servo1;

enum State
{
    BALL_PRESENT,
    VERIFYING,
    WAITING_FOR_BALL
} ;
State state = BALL_PRESENT;
unsigned long lastEventTime = 0;

bool prev_ball_state = false;

void setup()
{
    Serial.begin(115200);

    pinMode(SWITCH_PIN, INPUT_PULLUP);

    servo1.attach(SERVO_PIN);
    servo1.write(HOME_POS);

    Serial.println("Switch-to-servo test started");
}

void loop()
{   
    if (Serial.available()) {
        String cmd = Serial.readStringUntil('\n');
        cmd.trim();

        if (cmd == "HELLO") {
            Serial.println("ESP32_ALIVE");
        }

        else if (cmd == "FEED_ONE") {
            Serial.println("Feeding ball");

            servo1.write(FEED_POS);
            delay(750);

            servo1.write(HOME_POS);

            Serial.println("DONE");
        }
    }

    bool ball_state = (digitalRead(SWITCH_PIN) == LOW);
    unsigned long now = millis();


    if (ball_state != prev_ball_state && (now - lastEventTime > DEBOUNCE_MS)) {
        prev_ball_state = ball_state;

        if (ball_state) {
            Serial.println("BALL_PRESENT");
        } else {
            Serial.println("BALL_MISSING");
        }

        lastEventTime = now;
    }


    // if (!ball_state && state == BALL_PRESENT && (now - lastEventTime > DEBOUNCE_MS))
    // {
    //     Serial.println("FEED_ONE");

    //     servo1.write(FEED_POS);
    //     delay(750);

    //     servo1.write(HOME_POS);

    //     state = VERIFYING;
    //     lastEventTime = now;
    // }

    // else if (state == VERIFYING && (now - lastEventTime > check_time)) {
    //     lastEventTime = now;

    //     if (ball_state) {
    //         Serial.println("Feeding Complete");
    //         state = BALL_PRESENT;
    //         feed_attempt = 0;
    //     }

    //     else if (feed_attempt < 2){
    //         Serial.println("Feeding failed, try again.");
    //         state = BALL_PRESENT;
    //         feed_attempt++;
    //     } 

    //     else {
    //         Serial.println("Failed to feed, please placed the ball manually.");
    //         lastEventTime = now;
    //         state = WAITING_FOR_BALL;
    //     }

    // } 
    
    // if (state == WAITING_FOR_BALL && ball_state) {
    //     Serial.println("Ball manually placed on the tee, thank you");
    //     state = BALL_PRESENT;
    //     feed_attempt = 0;
    //     lastEventTime = now;
    // }

}