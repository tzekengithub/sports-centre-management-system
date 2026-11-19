import os, shutil, re, html, struct
BASE = os.path.expanduser("~/mnt/Sports Centre System/Report Support")
SRC = os.path.join(BASE, "Screenshots_Real")
ANN = os.path.join(SRC, "Annotated")
OUT = os.path.join(BASE, "Screenshots_Per_Person")
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
OWN = {"B": ("1_Teh_Tze_Ken_Booking_and_Home", "Teh Tze Ken", "Booking + Home"),
       "M": ("2_Teoh_Zynn_Membership", "Teoh Zynn", "Membership"),
       "C": ("3_Tan_Chor_Koon_Coaching", "Tan Chor Koon", "Coaching"),
       "L": ("4_Low_Yee_Zhe_Billing", "Low Yee Zhe", "Billing")}
A4 = "A.4 Features and GUI Screenshots"
S2 = "A.4.2 Module 1: Booking"; S3 = "A.4.3 Module 2: Membership"; S4 = "A.4.4 Module 3: Coaching"; S5 = "A.4.5 Module 4: Billing"
M0 = "C.2 Starting the Program"; M1 = "C.3.1 Booking"; M2 = "C.3.2 Membership"; M3 = "C.3.3 Coaching"; M4 = "C.3.4 Billing"
# (figure label, sort key, caption, section, owner, source file, kind, note)
F = []
def add(label, key, cap, sec, o, src, kind, note=""):
    F.append(dict(label=label, key=key, cap=cap, sec=sec, o=o, src=src, kind=kind, note=note))
sysp = [("1","Home tab of the main window",A4,"B"),("2","Dark mode (Book a Court page)",A4,"B"),("3","Book a Court page",S2,"B"),
 ("4","Reschedule Booking page",S2,"B"),("5","Cancel a Booking page",S2,"B"),("6","View All Bookings page",S2,"B"),
 ("7","Register page",S3,"M"),("8","Manage Members page",S3,"M"),("9","Renew Membership page",S3,"M"),
 ("10","Manage Coaches page",S4,"C"),("11","Manage Classes page",S4,"C"),("12","Enrol Member page",S4,"C"),
 ("13","Remove Member page",S4,"C"),("14","Hours & Commission page",S4,"C"),("15","Create Bill page",S5,"L"),
 ("16","Pay Bill page",S5,"L"),("17","Void Bill page",S5,"L"),("18","Delete Bill page",S5,"L"),
 ("19","View Receipt page",S5,"L"),("20","Daily Revenue page",S5,"L")]
for n, cap, sec, o in sysp:
    add("Figure "+n, (int(n),0), cap, sec, o, "Figure_%02d.png" % int(n), "A4", 'The picture shows the Book a Court page in dark mode. The doc caption says "Home tab": change it.' if n=="2" else "")
subs = [("8a",8,1,"Update a member (saved pop-up)",S3,"M","Figure_08a_update_member.png",""),
 ("8b",8,2,"Delete a member (confirmation pop-up)",S3,"M","Figure_08b_delete_member_confirm.png",""),
 ("10a",10,1,"Add a coach (saved pop-up)",S4,"C","Figure_10a_add_coach.png","The picture shows the success pop-up, so use this caption. The yellow placeholder in the doc says 'form filled in': change it."),
 ("10b",10,2,"Update a coach",S4,"C","Figure_10b_update_coach.png",""),
 ("10c",10,3,"Delete a coach (confirmation pop-up)",S4,"C","Figure_10c_delete_coach_confirm.png",""),
 ("11a",11,1,"Schedule a class (saved pop-up)",S4,"C","Figure_11a_schedule_class.png","The picture shows the success pop-up, so use this caption. The yellow placeholder in the doc says 'form filled in': change it."),
 ("11b",11,2,"Update a class",S4,"C","Figure_11b_update_class.png",""),
 ("11c",11,3,"Delete a class (confirmation pop-up)",S4,"C","Figure_11c_delete_class_confirm.png","")]
for lab, n, k, cap, sec, o, src, note in subs:
    add("Figure "+lab, (n,k), cap, sec, o, src, "A4", note)
man = [("54","The program after starting",M0,"B"),("55","Action menu of the Booking tab",M1,"B"),("56","Book a Court",M1,"B"),
 ("57","Reschedule a Booking",M1,"B"),("58","Cancel a Booking",M1,"B"),("59","View All Bookings",M1,"B"),
 ("60","Action menu of the Membership tab",M2,"M"),("61","Register a Member",M2,"M"),("62","Manage Members",M2,"M"),("63","Renew Membership",M2,"M"),
 ("64","Action menu of the Coaching tab",M3,"C"),("65","Manage Coaches",M3,"C"),("66","Manage Classes",M3,"C"),
 ("67","Enrol Member",M3,"C"),("68","Remove Member",M3,"C"),("69","Hours & Commission",M3,"C"),
 ("70","Action menu of the Billing tab",M4,"L"),("71","Create a Bill",M4,"L"),("72","Pay a Bill",M4,"L"),
 ("73","Void a Bill",M4,"L"),("74","View a Receipt",M4,"L"),("75","Daily Revenue",M4,"L")]
for n, cap, sec, o in man:
    add("Figure "+n, (int(n),0), cap, sec, o, "Figure_%s.png" % n, "MAN")
pops = [("Popup_success_booking_made.png","Pop-up: booking confirmed","B","after Figure 56 (Book a Court)"),
 ("Popup_error_booking_in_past.png","Pop-up error: date is in the past","B","after Figure 57 (Reschedule)"),
 ("Popup_confirm_cancel_booking.png","Pop-up question: cancel (part of) a booking?","B","after Figure 58 (Cancel)"),
 ("Popup_success_booking_cancelled.png","Pop-up: whole booking cancelled","B","after Figure 58 (Cancel)"),
 ("Popup_success_booking_part_cancelled.png","Pop-up: part of a booking cancelled","B","after Figure 58 (Cancel)"),
 ("Popup_error_cancel_blocked_bill.png","Pop-up error: booking has a bill, can't cancel","B","after Figure 58 (Cancel)"),
 ("Popup_success_member_registered.png","Pop-up: member registered","M","after Figure 61 (Register)"),
 ("Popup_error_member_delete_blocked.png","Pop-up error: member can't be deleted","M","after Figure 8b / Figure 62 (Manage Members)"),
 ("Figure_08b2_delete_member_done.png","Pop-up: member deleted","M","after Figure 8b (Delete a member)"),
 ("Popup_error_class_full.png","Pop-up error: class is full","C","after Figure 67 (Enrol Member)"),
 ("Popup_confirm_remove_member.png","Pop-up question: remove member from class?","C","after Figure 68 (Remove Member)"),
 ("Popup_error_coach_double_booked.png","Pop-up error: coach already has a class then","C","after Figure 66 (Manage Classes)"),
 ("Popup_success_bill_paid.png","Pop-up: bill paid","L","after Figure 72 (Pay a Bill)"),
 ("Popup_success_receipt_shown.png","Pop-up: receipt shown","L","after Figure 74 (View a Receipt)")]
for src, cap, o, where in []:
    add("Extra pop-up", (999, len(F)), cap, "Extra pictures (not in the doc yet)", o, src, "POP", "Suggested place: "+where+". Optional.")
def slug(s): return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
def size(p):
    d = open(p, "rb").read(24); return struct.unpack(">II", d[16:24])
kinddir = {"A4": "A4_System_pages", "MAN": "C3_User_manual_with_arrows", "POP": "Extra_popups"}
rows = []
for e in F:
    folder = OWN[e["o"]][0]; sub = kinddir[e["kind"]]
    os.makedirs(os.path.join(OUT, folder, sub), exist_ok=True)
    srcp = os.path.join(SRC, e["src"]); used = "plain"
    if e["kind"] == "MAN" and os.path.exists(os.path.join(ANN, e["src"])):
        srcp = os.path.join(ANN, e["src"]); used = "with arrows"
    if e["kind"] == "POP":
        base = e["src"][:-4].replace("Figure_08b2_delete_member_done", "Popup_success_member_deleted")
        name = base + ".png"
    else:
        num = e["label"].split(" ")[1]
        m = re.match(r"(\d+)(.*)", num); name = "Fig_%02d%s_%s.png" % (int(m.group(1)), m.group(2), slug(e["cap"]))
    dst = os.path.join(OUT, folder, sub, name); shutil.copy2(srcp, dst)
    w, h = size(dst); e.update(rel=folder+"/"+sub+"/"+name, used=used, w=w, h=h)
    if w < 600: e["note"] = (e["note"]+" " if e["note"] else "") + "Small picture (%dx%d): only the pop-up box. Fine to paste; make it narrower in the doc." % (w, h)

F.sort(key=lambda e: e["key"])
import html
GREET={"B":"Tze Ken","M":"Zynn","C":"Chor Koon","L":"Yee Zhe"}
def row(e):
    rel=e["rel"].split("/",1)[1]
    return ('<tr><td class="c"><input type="checkbox" data-k="%s"></td><td><b>%s</b></td><td><a href="%s" target="_blank"><img src="%s"></a></td>'
            '<td><div class="cap" id="cap%d">%s</div><button onclick="cp(\'cap%d\',this)">Copy caption</button></td><td>%s</td><td class="f">%s<br><small>%s</small></td><td class="n">%s</td></tr>') % (
        html.escape(e["rel"]), html.escape(e["label"]), html.escape(rel), html.escape(rel), id(e)%100000,
        html.escape(e["label"]+": "+e["cap"]), id(e)%100000, html.escape(e["sec"]), html.escape(rel.split("/")[-1]), e["used"], html.escape(e["note"]))
CSS="""body{font-family:"Segoe UI",Arial,sans-serif;margin:24px;color:#1f2a44;background:#f6f8f6}h1{color:#2e6b4b}h2{margin-top:30px;color:#2e6b4b;border-bottom:2px solid #2e6b4b}
table{border-collapse:collapse;width:100%;background:#fff}td,th{border:1px solid #ccd;padding:8px;vertical-align:top;font-size:14px}th{background:#2e6b4b;color:#fff}
img{width:260px;border:1px solid #999}.cap{font-family:"Times New Roman",serif;font-size:15px;margin-bottom:6px}.c{text-align:center}.n{color:#a33;max-width:230px}.f{font-size:12px;word-break:break-all}
button{cursor:pointer}.box{background:#fff;border-left:5px solid #2e6b4b;padding:10px 16px;margin:12px 0}"""
JS="""function cp(id,b){var t=document.getElementById(id).innerText;var a=document.createElement("textarea");a.value=t;document.body.appendChild(a);a.select();try{document.execCommand("copy");b.innerText="Copied"}catch(e){b.innerText="Select and copy"}document.body.removeChild(a);setTimeout(function(){b.innerText="Copy caption"},1200)}
var cs=document.querySelectorAll("input[type=checkbox]");for(var i=0;i<cs.length;i++){(function(c){try{c.checked=localStorage.getItem("done:"+c.dataset.k)=="1"}catch(e){}c.onchange=function(){try{localStorage.setItem("done:"+c.dataset.k,c.checked?"1":"0")}catch(e){}}})(cs[i])}"""
import zipfile
for o,(folder,name,mod) in OWN.items():
    es=[e for e in F if e["o"]==o]
    a4=[e for e in es if e["kind"]=="A4"]; mn=[e for e in es if e["kind"]=="MAN"]
    body=['<h1>Hi %s, these are your pictures (%s)</h1>' % (GREET[o], html.escape(mod)),
      '<div class="box"><b>Your job: %d pictures</b> (%d for Section A.4 system GUI, %d for Section C.3 user manual).<ol>'
      '<li>Open the Google Doc and press Ctrl+F for the figure number (for example <i>Figure %s</i>).</li>'
      '<li>Delete the yellow <i>[Paste screenshot here]</i> line, then paste the picture: Insert &gt; Image &gt; Upload from computer, about 15 cm wide.</li>'
      '<li>Check the caption under it matches the one below (use Copy caption). Tick Done.</li></ol>'
      '<p>The user manual pictures already have the red circles and arrows.</p></div>' % (len(es),len(a4),len(mn),(mn[0]["label"].split(" ")[1] if mn else ""))]
    for title,lst in (("Section A.4: System GUI screenshots",a4),("Section C.3: User manual screenshots",mn)):
        body.append("<h2>%s (%d)</h2><table><tr><th>Done</th><th>Figure</th><th>Picture (click to enlarge)</th><th>Caption to type under it</th><th>Where in the report</th><th>File</th><th>Note</th></tr>%s</table>" % (title,len(lst),"".join(row(e) for e in lst)))
    page="<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>%s: your screenshots</title><style>%s</style></head><body>%s<script>%s</script></body></html>" % (html.escape(name),CSS,"".join(body),JS)
    open(os.path.join(OUT,folder,"START_HERE.html"),"w",encoding="utf-8").write(page)
    # personal zip
    zp=os.path.join(os.path.expanduser("~/tmp_org"),folder+".zip")
    if os.path.exists(zp): os.remove(zp)
    with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
        for root,_,files in os.walk(os.path.join(OUT,folder)):
            for fn in files:
                full=os.path.join(root,fn); z.write(full,os.path.join(folder,os.path.relpath(full,os.path.join(OUT,folder))))
    print(folder,len(es),os.path.getsize(zp))
