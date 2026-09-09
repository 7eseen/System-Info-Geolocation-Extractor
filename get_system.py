import json
import os
import platform
import socket
import urllib.request


def get_system_info():
    """استخراج معلومات الجهاز ونظام التشغيل"""
    info = {
        "اسم الجهاز (Hostname)": socket.gethostname(),
        "نظام التشغيل": platform.system(),
        "إصدار النظام": platform.release(),
        "تفاصيل الاصدار": platform.version(),
        "المعمارية": platform.machine(),
        "المعالج": platform.processor(),
        "اسم المستخدم": os.getlogin()
        if hasattr(os, "getlogin")
        else os.environ.get("USER", "N/A"),
    }

    # جلب عنوان الـ IP المحلي
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        info["الـ IP المحلي (Local IP)"] = s.getsockname()[0]
        s.close()
    except Exception:
        info["الـ IP المحلي (Local IP)"] = "غير قادر على التحديد"

    return info


def get_geo_location():
    """جلب عنوان الـ IP الخارجي والموقع الجغرافي التقريبي"""
    try:
        # استخدام خدمة ip-api المجانية التي ترجع البيانات بصيغة JSON
        url = "http://ip-api.com/json/"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())

            if data.get("status") == "success":
                return {
                    "الـ IP الخارجي (Public IP)": data.get("query"),
                    "الدولة": data.get("country"),
                    "المدينة": data.get("city"),
                    "المنطقة": data.get("regionName"),
                    "مزود الخدمة (ISP)": data.get("isp"),
                    "خطوط الطول والعرض": f"{data.get('lat')}, {data.get('lon')}",
                    "المنطقة الزمنية": data.get("timezone"),
                }
            else:
                return {
                    "خطأ": "فشل جلب تفاصيل الموقع من المزود."
                }
    except Exception as e:
        return {"خطأ": f"فشل الاتصال بالشبكة: {e}"}


def main():
    print("=" * 50)
    print("        مشروع مستخرج معلومات النظام والموقع        ")
    print("=" * 50)

    print("\n[+] جاري جمع معلومات النظام...")
    sys_info = get_system_info()
    for key, value in sys_info.items():
        print(f" - {key}: {value}")

    print("\n[+] جاري تحديد الموقع الجغرافي...")
    geo_info = get_geo_location()
    for key, value in geo_info.items():
        print(f" - {key}: {value}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()