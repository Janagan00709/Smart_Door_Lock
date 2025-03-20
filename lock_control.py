from flask import Blueprint, render_template, request, redirect, url_for
import RPi.GPIO as GPIO
import csv

LOCK_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LOCK_PIN, GPIO.OUT)

lock_routes = Blueprint('lock', __name__, url_prefix='/lock')

def lock_door():
    GPIO.output(LOCK_PIN, GPIO.HIGH)
    print("🔒 Door Locked")

def unlock_door():
    GPIO.output(LOCK_PIN, GPIO.LOW)
    print("🔓 Door Unlocked")

def check_lock_status():
    return "Locked" if GPIO.input(LOCK_PIN) == GPIO.HIGH else "Unlocked"

@lock_routes.route('/dashboard')
def dashboard():
    lock_status = check_lock_status()
    return render_template('dashboard.html', lock_status=lock_status)

@lock_routes.route('/toggle', methods=['POST'])
def toggle_lock():
    action = request.form['action']
    if action == "Lock":
        lock_door()
    elif action == "Unlock":
        unlock_door()
    return redirect(url_for('lock.dashboard'))

@lock_routes.route('/schedule', methods=['POST'])
def update_schedule():
    new_time = request.form['new_time']
    with open('holidays.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([new_time, "Custom Schedule"])
    print(f"✅ Schedule updated to: {new_time}")
    return redirect(url_for('lock.dashboard'))
