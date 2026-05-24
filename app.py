from flask import Flask, render_template_string, request, redirect, url_for, flash
import datetime

app = Flask(__name__)
app.secret_key = "super_secret_hotel_key_123"

# 1. CURRENCY UPDATE: Changed sample base prices to INR values
hotel_data = {
    "rooms": {
        "101": {"type": "Standard Single", "price": "2,500", "status": "Available", "guest": ""},
        "102": {"type": "Standard Single", "price": "2,500", "status": "Available", "guest": ""},
        "201": {"type": "Deluxe Double", "price": "4,500", "status": "Available", "guest": ""},
        "202": {"type": "Deluxe Double", "price": "4,500", "status": "Available", "guest": ""},
        "301": {"type": "Executive Suite", "price": "9,000", "status": "Available", "guest": ""},
    },
    "bookings": []
}

# 2. CREATIVE VISUAL DESIGN: Premium Dark Theme UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grand Horizon Premier Cloud</title>
    <style>
        * { box-sizing: border-box; font-family: 'Inter', system-ui, -apple-system, sans-serif; margin: 0; padding: 0; }
        
        /* Deep midnight background with subtle radial gradient for depth */
        body { 
            background: radial-gradient(circle at top right, #111827, #070a12); 
            color: #f3f4f6; 
            padding: 30px 20px;
            min-height: 100vh;
        }
        
        .container { max-width: 1200px; margin: 0 auto; }
        
        /* Sleek minimalist header */
        header { 
            text-align: center; 
            margin-bottom: 35px; 
            border-bottom: 1px solid #1e293b;
            padding-bottom: 25px;
        }
        header h1 { font-size: 2.2rem; font-weight: 700; letter-spacing: -0.05em; color: #fff; margin-bottom: 6px; }
        header p { color: #64748b; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.1em; }
        
        .grid { display: grid; grid-template-columns: 1.6fr 1.1fr; gap: 25px; }
        @media (max-width: 900px) { .grid { grid-template-columns: 1fr; } }
        
        /* Glassmorphism card panels */
        .card { 
            background: rgba(15, 23, 42, 0.6); 
            backdrop-filter: blur(8px);
            padding: 25px; 
            border-radius: 12px; 
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3); 
            margin-bottom: 25px; 
        }
        
        h2 { font-size: 1.25rem; font-weight: 600; margin-bottom: 20px; color: #f8fafc; display: flex; align-items: center; gap: 10px; }
        
        /* Grid container for individual rooms */
        .room-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
        
        /* Individual room layout changes */
        .room-box { 
            border-radius: 10px; 
            background: #111c30;
            border: 1px solid #1e293b;
            text-align: left; 
            position: relative; 
            padding: 20px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .room-box:hover { transform: translateY(-4px); border-color: #3b82f6; box-shadow: 0 8px 20px rgba(59,130,246,0.15); }
        
        /* Glowing neon visual indicators for room states */
        .Available { border-left: 4px solid #10b981; }
        .Occupied { border-left: 4px solid #ef4444; }
        
        .status-badge {
            font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
            display: inline-block; padding: 3px 8px; border-radius: 20px; margin-top: 10px;
        }
        .Available .status-badge { background: rgba(16, 185, 129, 0.1); color: #34d399; }
        .Occupied .status-badge { background: rgba(239, 68, 68, 0.1); color: #f87171; }
        
        .room-box h3 { font-size: 1.15rem; color: #fff; margin-bottom: 2px; }
        .room-type { font-size: 0.8rem; color: #94a3b8; margin-bottom: 12px; }
        .room-price { font-size: 1rem; font-weight: 600; color: #f1f5f9; }
        
        /* Premium looking Inputs and Buttons */
        .form-group { margin-bottom: 18px; }
        label { display: block; margin-bottom: 8px; color: #94a3b8; font-weight: 500; font-size: 0.85rem; }
        input, select { 
            width: 100%; padding: 12px; background: #0f172a; border: 1px solid #334155; 
            border-radius: 6px; font-size: 0.95rem; color: #fff; transition: 0.2s;
        }
        input:focus, select:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 2px rgba(59,130,246,0.2); }
        
        button { 
            width: 100%; padding: 14px; background: #3b82f6; color: white; border: none; 
            border-radius: 6px; font-weight: 600; font-size: 0.95rem; cursor: pointer; transition: all 0.2s; 
        }
        button:hover { background: #2563eb; box-shadow: 0 4px 12px rgba(59,130,246,0.3); }
        
        .btn-checkout { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); padding: 6px 12px; font-size: 0.8rem; border-radius: 4px; cursor: pointer; margin-top: 12px; width: auto;}
        .btn-checkout:hover { background: #ef4444; color: white; }
        
        /* Banner system notices */
        .alert { background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.3); color: #60a5fa; padding: 14px; border-radius: 6px; margin-bottom: 20px; font-weight: 500; text-align: center;}
        
        /* Micro-designed Data Log Tables */
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem; }
        th, td { padding: 12px 14px; text-align: left; border-bottom: 1px solid #1e293b; }
        th { background: #0f172a; color: #94a3b8; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em;}
        td { color: #cbd5e1; }
        tr:hover td { background: rgba(255,255,255,0.01); }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔮 GRAND HORIZON</h1>
            <p>Core Intelligence System Terminal</p>
        </header>

        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <div class="alert">⚡ {{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <div class="grid">
            <div class="card">
                <h2><span>🔑</span> Real-Time Room Matrix</h2>
                <div class="room-grid">
                    {% for num, info in data.rooms.items() %}
                        <div class="room-box {{ info.status }}">
                            <h3>Room {{ num }}</h3>
                            <div class="room-type">{{ info.type }}</div>
                            <div class="room-price">₹{{ info.price }} <span style="font-size:0.75rem; color:#64748b;">/ night</span></div>
                            <div class="status-badge">{{ info.status }}</div>
                            
                            {% if info.status == 'Occupied' %}
                                <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 12px; border-top: 1px dashed #1e293b; padding-top: 8px;">
                                    Guest: <strong style="color: #f1f5f9;">{{ info.guest }}</strong>
                                </p>
                                <form action="/checkout/{{ num }}" method="POST">
                                    <button type="submit" class="btn-checkout">Release Room</button>
                                </form>
                            {% endif %}
                        </div>
                    {% endfor %}
                </div>
            </div>

            <div>
                <div class="card">
                    <h2><span>📝</span> Rapid Check-In Protocol</h2>
                    <form action="/checkin" method="POST">
                        <div class="form-group">
                            <label>Primary Guest Name</label>
                            <input type="text" name="guest_name" required placeholder="Ex: Amit Sharma">
                        </div>
                        <div class="form-group">
                            <label>Allocate Desired Suite</label>
                            <select name="room_num" required>
                                {% for num, info in data.rooms.items() %}
                                    {% if info.status == 'Available' %}
                                        <option value="{{ num }}">Room {{ num }} - {{ info.type }} (₹{{ info.price }})</option>
                                    {% endif %}
                                {% endfor %}
                            </select>
                        </div>
                        <button type="submit">Deploy Guest Check-In</button>
                    </form>
                </div>

                <div class="card">
                    <h2><span>⏳</span> Transaction Audits</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Profile</th>
                                <th>Room</th>
                                <th>Status</th>
                                <th>Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for b in data.bookings[::-1][:4] %}
                            <tr>
                                <td style="font-weight: 500; color: #fff;">{{ b.guest }}</td>
                                <td><span style="background: #1e293b; padding: 2px 6px; border-radius: 4px;">{{ b.room }}</span></td>
                                <td>
                                    <span style="color: {{ '#34d399' if b.action == 'Checked In' else '#f87171' }};">
                                        {{ b.action }}
                                    </span>
                                </td>
                                <td style="font-size: 0.8rem; color: #64748b;">{{ b.time.split(' ')[1] }}</td>
                            </tr>
                            {% else %}
                            <tr>
                                <td colspan="4" style="text-align: center; color: #64748b; padding: 20px 0;">System idle. No recent cycles.</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE, data=hotel_data)

@app.route('/checkin', methods=['POST'])
def checkin():
    guest_name = request.form.get('guest_name')
    room_num = request.form.get('room_num')
    
    if room_num in hotel_data['rooms'] and hotel_data['rooms'][room_num]['status'] == 'Available':
        hotel_data['rooms'][room_num]['status'] = 'Occupied'
        hotel_data['rooms'][room_num]['guest'] = guest_name
        
        hotel_data['bookings'].append({
            "guest": guest_name,
            "room": room_num,
            "action": "Checked In",
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        flash(f"Successfully checked in {guest_name} to Room {room_num}!")
    return redirect(url_for('dashboard'))

@app.route('/checkout/<room_num>', methods=['POST'])
def checkout(room_num):
    if room_num in hotel_data['rooms'] and hotel_data['rooms'][room_num]['status'] == 'Occupied':
        guest_name = hotel_data['rooms'][room_num]['guest']
        hotel_data['rooms'][room_num]['status'] = 'Available'
        hotel_data['rooms'][room_num]['guest'] = ""
        
        hotel_data['bookings'].append({
            "guest": guest_name,
            "room": room_num,
            "action": "Checked Out",
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        flash(f"Room {room_num} cleared. Guest {guest_name} checked out successfully.")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run()

