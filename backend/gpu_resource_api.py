from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

# 사용자 더미 (15명)
users = [
    "홍길동", "김철수", "김동현", "김서권", "윤다빈",
    "박지훈", "최예린", "이민호", "한지수", "조윤호",
    "정소연", "오세훈", "서지수", "배상우", "노지윤"
]

# GPU, CPU, Memory (20개)
gpu_models = [f"NVIDIA RTX 40{str(i%5+70)} Ti" for i in range(20)]
cpu_models = [f"Intel Xeon {i+1}900X" for i in range(20)]
gpu_names = [f"GPU{i+1}" for i in range(20)]
cpu_names = [f"CPU{i+1}" for i in range(20)]
memory_names = [f"MEM{i+1}" for i in range(20)]

resources = []
for i in range(20):
    resources.append({"res_id": i, "type": "GPU", "model": gpu_models[i], "name": gpu_names[i]})
    resources.append({"res_id": i, "type": "CPU", "model": cpu_models[i], "name": cpu_names[i]})
    resources.append({"res_id": i, "type": "Memory", "model": "Samsung DDR4", "name": memory_names[i]})

memory_total_tb = 20

# --- 자원 할당/회수 더미 데이터 (in-memory) ---
allocations = []
# 예시 데이터: 일부만 미리 할당
for i in range(10):  # GPU
    allocations.append({
        "res_id": i, "type": "GPU", "user": users[i], 
        "start_date": "2024-07-01", "end_date": "2024-07-20"
    })
for i in range(5):  # CPU
    allocations.append({
        "res_id": i, "type": "CPU", "user": users[i+5], 
        "start_date": "2024-07-02", "end_date": "2024-07-16"
    })
for i in range(3):  # Memory
    allocations.append({
        "res_id": i, "type": "Memory", "user": users[i+8],
        "start_date": "2024-07-05", "end_date": "2024-07-19"
    })

memory_usage_gb = [random.randint(200, 900) for _ in range(20)]  # 1TB=1000GB

# ----------------
# 자원 할당/회수/목록 관련 기존 API (복원)
@app.route("/api/resources", methods=["GET"])
def get_resources():
    result = []
    for r in resources:
        alloc = next((a for a in allocations if a["res_id"] == r["res_id"] and a["type"] == r["type"]), None)
        row = {**r}
        if alloc:
            row.update({k: alloc[k] for k in ["user", "start_date", "end_date"]})
        else:
            row.update({"user": None, "start_date": None, "end_date": None})
        result.append(row)
    return jsonify(result)

@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/api/allocations", methods=["POST"])
def allocate_resource():
    data = request.json
    for a in allocations:
        if a["res_id"] == data["res_id"] and a["type"] == data["type"]:
            return jsonify({"result": "already_allocated"})
    allocations.append({
        "res_id": data["res_id"],
        "type": data["type"],
        "user": data["user"],
        "start_date": data["start_date"],
        "end_date": data["end_date"]
    })
    return jsonify({"result": "success"})

@app.route("/api/allocations/reclaim", methods=["POST"])
def reclaim_resource():
    data = request.json
    global allocations
    allocations = [a for a in allocations if not (a["res_id"] == data["res_id"] and a["type"] == data["type"])]
    return jsonify({"result": "success"})

# ----------------
# 보고서 관련 API (변경 없음)
@app.route("/api/report/sysinfo")
def sysinfo():
    gpu_used = len([a for a in allocations if a['type'] == 'GPU'])
    cpu_used = len([a for a in allocations if a['type'] == 'CPU'])
    memory_used = len([a for a in allocations if a['type'] == 'Memory'])
    return jsonify({
        "user_count": len(users),
        "gpu_count": 20,
        "cpu_count": 20,
        "memory_count": 20,
        "memory_total_tb": memory_total_tb,
        "gpu_used": gpu_used,
        "cpu_used": cpu_used,
        "memory_used": memory_used,
        "gpu_models": list(set(gpu_models)),
        "cpu_models": list(set(cpu_models))
    })

@app.route("/api/report/total_usage")
def total_usage():
    dates = [(datetime(2024,7,1)+timedelta(days=i)).strftime("%Y-%m-%d") for i in range(20)]
    gpu_usage = [random.randint(10,20) for _ in dates]
    cpu_usage = [random.randint(5,15) for _ in dates]
    memory_usage = [random.randint(12,20) for _ in dates]
    return jsonify({
        "dates": dates,
        "gpu": gpu_usage,
        "cpu": cpu_usage,
        "memory": memory_usage
    })

@app.route("/api/report/status")
def status():
    gpu_temps = [random.randint(35, 85) for _ in range(5)]
    cpu_temps = [random.randint(35, 90) for _ in range(5)]
    memory_usages = [random.randint(40, 100) for _ in range(5)]
    return jsonify({
        "gpu_names": gpu_names[:5],
        "cpu_names": cpu_names[:5],
        "memory_names": memory_names[:5],
        "gpu_temps": gpu_temps,
        "cpu_temps": cpu_temps,
        "memory_usages": memory_usages
    })

@app.route("/api/report/individual_usage")
def individual_usage():
    rtype = request.args.get("type")
    name = request.args.get("name")
    dates = [(datetime(2024,7,1)+timedelta(days=i)).strftime("%Y-%m-%d") for i in range(20)]
    values = [random.randint(2, 20) if rtype!="Memory" else random.randint(40,100) for _ in dates]
    return jsonify({
        "dates": dates,
        "values": values
    })

@app.route("/api/report/rank")
def report_rank():
    user_usage = []
    for i, uname in enumerate(users):
        gpu = random.randint(0, 25)
        cpu = random.randint(0, 25)
        memory = random.randint(0, 25)
        idle = random.randint(0, 20)
        user_usage.append({
            "name": uname, "gpu": gpu, "cpu": cpu, "memory": memory, "idle": idle
        })
    usage_rank = sorted(user_usage, key=lambda x: (x['gpu']+x['cpu']+x['memory']), reverse=True)[:5]
    idle_rank = sorted(user_usage, key=lambda x: x['idle'], reverse=True)[:5]
    return jsonify({"usage": usage_rank, "idle": idle_rank})

if __name__ == "__main__":
    app.run(debug=True)
