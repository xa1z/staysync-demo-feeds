# Generates demo .ics feeds from scenario.json. Each unit: airbnb-<key>.ics and gathern-<key>.ics
import json, hashlib, datetime, sys
sc=json.load(open('scenario.json',encoding='utf-8'))
def dt(d): return d.replace('-','')
def ev(uid, summary, start, end, desc):
    stamp=datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    desc=desc.replace('\n','\\n')
    return f"BEGIN:VEVENT\nDTSTAMP:{stamp}\nDTSTART;VALUE=DATE:{dt(start)}\nDTEND;VALUE=DATE:{dt(end)}\nSUMMARY:{summary}\nUID:{uid}\nDESCRIPTION:{desc}\nEND:VEVENT\n"
for key,u in sc['units'].items():
    for src in ('airbnb','gathern'):
        body=""
        for e in u.get(src,[]):
            h=hashlib.md5(f"{key}{src}{e['start']}{e['end']}{e.get('id','')}".encode()).hexdigest()[:16]
            if e.get('block'):
                if src=='airbnb':
                    body+=ev(f"{h}@airbnb.com","Airbnb (Not available)",e['start'],e['end'],"")
                else:
                    body+=ev(f"{h}@gathern.co","Blocked",e['start'],e['end'],"")
            else:
                if src=='airbnb':
                    body+=ev(f"{h}@airbnb.com","Reserved",e['start'],e['end'],f"Reservation URL: https://www.airbnb.com/hosting/reservations/details/{e['id']}\nPhone Number (Last 4 Digits): {e.get('last4','0000')}")
                else:
                    body+=ev(f"{h}@gathern.co","Reserved",e['start'],e['end'],f"Booking ID: {e['id']}\nGuest: {e.get('guest','')}\nPhone Number: {e.get('phone','+966500000000')}")
        prod="-//Airbnb Inc//Hosting Calendar 0.8.8//EN" if src=='airbnb' else "-//Gathern//Calendar//EN"
        cal=f"BEGIN:VCALENDAR\nPRODID:{prod}\nCALSCALE:GREGORIAN\nVERSION:2.0\n{body}END:VCALENDAR\n"
        open(f"{src}-{key}.ics","w",encoding="utf-8").write(cal)
print("ok", len(sc['units']))
