from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

# -- 더미 유저/자원
users = [
    '홍길동', '김철수', '김동현', '김서권', '윤다빈',
    '박지훈', '최예린', '이민호', '한지수', '조윤호',
    '정소연', '오세훈', '서지수', '배상우', '노지윤'
]
gpus = [{"res_id": i, "type": "GPU", "model": f"RTX 4090 {i+1}", "name": f"GPU-{i+1}"} for i in range(20)]
cpus = [{"res_id": i, "type": "CPU", "model": f"Xeon Gold 6{str(i).zfill(2)}", "name": f"CPU-{i+1}"} for i in range(20)]
memories = [{"res_id": i, "type": "Memory", "size": 1, "name": f"Memory-{i+1}"} for i in range(20)]
resources = gpus + cpus + memories

# -- 할당 대량 생성 (더미)
def random_allocations():
    allocs = []
    base = datetime(2024, 7, 1)
    for tlist, typename in [(gpus, "GPU"), (cpus, "CPU"), (memories, "Memory")]:
        for res in tlist:
            if random.random() < 0.8:  # 80% 할당
                user = random.choice(users)
                day = random.randint(0, 25)
                duration = random.randint(3, 7)
                allocs.append({
                    "res_id": res["res_id"],
                    "type": typename,
                    "user": user,
                    "start_date": (base + timedelta(days=day)).strftime('%Y-%m-%d'),
                    "end_date": (base + timedelta(days=day+duration)).strftime('%Y-%m-%d')
                })
    return allocs
allocations = random_allocations()

@app.route("/api/report/sysinfo", methods=["GET"])
def get_sysinfo():
    gpu_models = sorted(set([r["model"] for r in gpus]))
    cpu_models = sorted(set([r["model"] for r in cpus]))
    return jsonify({
        "user_count": len(users),
        "gpu_count": len(gpus),
        "cpu_count": len(cpus),
        "memory_count": len(memories),
        "gpu_models": gpu_models,
        "cpu_models": cpu_models,
        "memory_total_tb": len(memories),
        "gpu_used": sum(1 for r in gpus if any(a for a in allocations if a["type"]=="GPU" and a["res_id"]==r["res_id"])),
        "cpu_used": sum(1 for r in cpus if any(a for a in allocations if a["type"]=="CPU" and a["res_id"]==r["res_id"])),
        "memory_used": sum(1 for r in memories if any(a for a in allocations if a["type"]=="Memory" and a["res_id"]==r["res_id"])),
    })

@app.route("/api/report/total_usage", methods=["GET"])
def total_usage():
    dates = [(datetime(2024,7,1) + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(31)]
    gpu = [0]*31
    cpu = [0]*31
    memory = [0]*31
    for a in allocations:
        s = datetime.strptime(a["start_date"], "%Y-%m-%d")
        e = datetime.strptime(a["end_date"], "%Y-%m-%d")
        for i, day in enumerate(dates):
            day_dt = datetime.strptime(day, "%Y-%m-%d")
            if s <= day_dt <= e:
                if a["type"] == "GPU":
                    gpu[i] += 1
                elif a["type"] == "CPU":
                    cpu[i] += 1
                elif a["type"] == "Memory":
                    memory[i] += 1
    return jsonify({
        "dates": dates,
        "gpu": gpu,
        "cpu": cpu,
        "memory": memory
    })

@app.route("/api/report/individual_usage", methods=["GET"])
def individual_usage():
    rtype = request.args.get("type")
    name = request.args.get("name")
    dates = [(datetime(2024,7,1) + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(31)]
    idx = int(name.split('-')[1]) - 1
    if rtype == "GPU":
        res = gpus[idx]
    elif rtype == "CPU":
        res = cpus[idx]
    else:
        res = memories[idx]
    vals = []
    for d in dates:
        is_used = 0
        for a in allocations:
            if a["type"] == rtype and a["res_id"] == res["res_id"]:
                s = datetime.strptime(a["start_date"], "%Y-%m-%d")
                e = datetime.strptime(a["end_date"], "%Y-%m-%d")
                cur = datetime.strptime(d, "%Y-%m-%d")
                if s <= cur <= e:
                    is_used = 1
                    break
        if rtype == "Memory":
            vals.append(is_used*random.randint(60,96))
        else:
            vals.append(is_used*random.uniform(0.3, 1.5))
    return jsonify({
        "dates": dates,
        "values": vals
    })

@app.route("/api/report/status", methods=["GET"])
def get_status():
    gpu_temps = [random.randint(30, 88) for _ in gpus]
    cpu_temps = [random.randint(32, 72) for _ in cpus]
    memory_usages = [random.randint(60, 96) for _ in memories]
    return jsonify({
        "gpu_temps": gpu_temps,
        "cpu_temps": cpu_temps,
        "memory_usages": memory_usages,
        "gpu_names": [g["name"] for g in gpus],
        "cpu_names": [c["name"] for c in cpus],
        "memory_names": [m["name"] for m in memories]
    })

@app.route("/api/report/rank", methods=["GET"])
def get_rank():
    rank = []
    for u in users:
        gpu_days = 0
        cpu_days = 0
        memory_days = 0
        for a in allocations:
            if a["user"] == u:
                s = datetime.strptime(a["start_date"], "%Y-%m-%d")
                e = datetime.strptime(a["end_date"], "%Y-%m-%d")
                days = (e-s).days + 1
                if a["type"] == "GPU":
                    gpu_days += days
                elif a["type"] == "CPU":
                    cpu_days += days
                elif a["type"] == "Memory":
                    memory_days += days
        rank.append({"name": u, "gpu": gpu_days, "cpu": cpu_days, "memory": memory_days})
    rank.sort(key=lambda x: (x["gpu"] + x["cpu"] + x["memory"]), reverse=True)
    return jsonify(rank)

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

if __name__ == "__main__":
    app.run(debug=True)
