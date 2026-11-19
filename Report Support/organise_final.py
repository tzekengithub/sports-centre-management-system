"""Builds Screenshots_Final/: one folder per team member with ONLY their pictures
(plain system pages for Section A.4, numbered-mark pictures from Annotated_v2 for
Section C.3), a personal START_HERE.html guide, and one zip per person.
Originals are copied, never moved or changed. Old output folders are MOVED to
_old_do_not_use/. Based on _reference_organise_per_person.py.
Run:  python organise_final.py"""

import hashlib
import html
import os
import re
import shutil
import struct
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "Screenshots_Real")
ANN2 = os.path.join(SRC, "Annotated_v2")
OUT = os.path.join(BASE, "Screenshots_Final")
OLD = os.path.join(BASE, "_old_do_not_use")
STEPS_FILE = os.path.join(SRC, "Manual_Steps_Matching_Marks.md")

OWN = {"B": ("1_Teh_Tze_Ken_Booking_and_Home", "Teh Tze Ken", "Booking + Home", "Tze Ken"),
       "M": ("2_Teoh_Zynn_Membership", "Teoh Zynn", "Membership", "Zynn"),
       "C": ("3_Tan_Chor_Koon_Coaching", "Tan Chor Koon", "Coaching", "Chor Koon"),
       "L": ("4_Low_Yee_Zhe_Billing", "Low Yee Zhe", "Billing", "Yee Zhe")}
A4 = "A.4 Features and GUI Screenshots"
S2, S3, S4, S5 = ("A.4.2 Module 1: Booking", "A.4.3 Module 2: Membership",
                  "A.4.4 Module 3: Coaching", "A.4.5 Module 4: Billing")
M0, M1, M2, M3, M4 = ("C.2 Starting the Program", "C.3.1 Booking", "C.3.2 Membership",
                      "C.3.3 Coaching", "C.3.4 Billing")
SUCCESS_NOTE = ("The picture shows the success pop-up, so use this caption. The yellow placeholder in the "
                "doc says 'form filled in': change it.")

FIGURES = []   # one dict per picture


def add(label, key, caption, section, owner, source, kind, note=""):
    """Register one picture."""
    FIGURES.append({"label": label, "key": key, "cap": caption, "sec": section, "o": owner,
                    "src": source, "kind": kind, "note": note})


system_pages = [
    ("1", "Home tab of the main window", A4, "B"), ("2", "Dark mode (Book a Court page)", A4, "B"),
    ("3", "Book a Court page", S2, "B"), ("4", "Reschedule Booking page", S2, "B"),
    ("5", "Cancel a Booking page", S2, "B"), ("6", "View All Bookings page", S2, "B"),
    ("7", "Register page", S3, "M"), ("8", "Manage Members page", S3, "M"), ("9", "Renew Membership page", S3, "M"),
    ("10", "Manage Coaches page", S4, "C"), ("11", "Manage Classes page", S4, "C"),
    ("12", "Enrol Member page", S4, "C"), ("13", "Remove Member page", S4, "C"),
    ("14", "Hours & Commission page", S4, "C"), ("15", "Create Bill page", S5, "L"),
    ("16", "Pay Bill page", S5, "L"), ("17", "Void Bill page", S5, "L"), ("18", "Delete Bill page", S5, "L"),
    ("19", "View Receipt page", S5, "L"), ("20", "Daily Revenue page", S5, "L")]
for number, caption, section, owner in system_pages:
    note = ""
    if number == "2":
        note = ('The picture shows the Book a Court page in dark mode. The doc caption says "Home tab": '
                "change it to the caption shown here.")
    add("Figure " + number, (int(number), 0), caption, section, owner, "Figure_%02d.png" % int(number), "A4", note)

sub_figures = [
    ("8a", 8, 1, "Update a member (saved pop-up)", S3, "M", "Figure_08a_update_member.png", ""),
    ("8b", 8, 2, "Delete a member (confirmation pop-up)", S3, "M", "Figure_08b_delete_member_confirm.png", ""),
    ("10a", 10, 1, "Add a coach (saved pop-up)", S4, "C", "Figure_10a_add_coach.png", SUCCESS_NOTE),
    ("10b", 10, 2, "Update a coach", S4, "C", "Figure_10b_update_coach.png", ""),
    ("10c", 10, 3, "Delete a coach (confirmation pop-up)", S4, "C", "Figure_10c_delete_coach_confirm.png", ""),
    ("11a", 11, 1, "Schedule a class (saved pop-up)", S4, "C", "Figure_11a_schedule_class.png", SUCCESS_NOTE),
    ("11b", 11, 2, "Update a class", S4, "C", "Figure_11b_update_class.png", ""),
    ("11c", 11, 3, "Delete a class (confirmation pop-up)", S4, "C", "Figure_11c_delete_class_confirm.png", "")]
for label, number, order, caption, section, owner, source, note in sub_figures:
    add("Figure " + label, (number, order), caption, section, owner, source, "A4", note)

manual_pages = [
    ("54", "The program after starting", M0, "B"), ("55", "Action menu of the Booking tab", M1, "B"),
    ("56", "Book a Court", M1, "B"), ("57", "Reschedule a Booking", M1, "B"), ("58", "Cancel a Booking", M1, "B"),
    ("59", "View All Bookings", M1, "B"), ("60", "Action menu of the Membership tab", M2, "M"),
    ("61", "Register a Member", M2, "M"), ("62", "Manage Members", M2, "M"), ("63", "Renew Membership", M2, "M"),
    ("64", "Action menu of the Coaching tab", M3, "C"), ("65", "Manage Coaches", M3, "C"),
    ("66", "Manage Classes", M3, "C"), ("67", "Enrol Member", M3, "C"), ("68", "Remove Member", M3, "C"),
    ("69", "Hours & Commission", M3, "C"), ("70", "Action menu of the Billing tab", M4, "L"),
    ("71", "Create a Bill", M4, "L"), ("72", "Pay a Bill", M4, "L"), ("73", "Void a Bill", M4, "L"),
    ("74", "View a Receipt", M4, "L"), ("75", "Daily Revenue", M4, "L")]
for number, caption, section, owner in manual_pages:
    add("Figure " + number, (int(number), 0), caption, section, owner, "Figure_%s.png" % number, "MAN")


def slug(text):
    """File-name friendly version of a caption."""
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")


def png_size(path):
    """Width and height of a PNG."""
    with open(path, "rb") as handle:
        header = handle.read(24)
    return struct.unpack(">II", header[16:24])


def sha(path):
    """SHA-256 of a file."""
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def read_steps():
    """Figure number -> list of step lines, from Manual_Steps_Matching_Marks.md."""
    text = open(STEPS_FILE, encoding="utf-8").read()
    parts = re.split(r"\*\*Figure (\d+):[^*]*\*\*", text)
    steps = {}
    for index in range(1, len(parts), 2):
        lines = []
        for line in parts[index + 1].splitlines():
            match = re.match(r"^(\d+)\. (.*)$", line.strip())
            if match:
                lines.append((int(match.group(1)), match.group(2)))
        steps[parts[index]] = lines
    return steps


def move_old_outputs():
    """Move the old output folders and zips into _old_do_not_use/ (never delete)."""
    os.makedirs(OLD, exist_ok=True)
    refused = []
    for name in ("Screenshots_Organised", "Screenshots_Organised.zip", "Screenshots_For_Report",
                 "Screenshots_For_Report.zip", "Screenshots_Per_Person", "Screenshots_Final"):
        source = os.path.join(BASE, name)
        if not os.path.exists(source):
            continue
        target = os.path.join(OLD, name if name != "Screenshots_Final" else "Screenshots_Final_earlier_attempt")
        if os.path.exists(target):
            refused.append(name + " (target already exists in _old_do_not_use)")
            continue
        try:
            shutil.move(source, target)
            print("moved", name, "->", os.path.relpath(target, BASE))
        except OSError as error:
            refused.append(f"{name} ({error})")
    return refused


CSS = """body{font-family:"Segoe UI",Arial,sans-serif;margin:24px;color:#1f2a44;background:#f6f8f6}h1{color:#2e6b4b}
h2{margin-top:30px;color:#2e6b4b;border-bottom:2px solid #2e6b4b}
table{border-collapse:collapse;width:100%;background:#fff}td,th{border:1px solid #ccd;padding:8px;vertical-align:top;font-size:14px}
th{background:#2e6b4b;color:#fff}img{width:260px;border:1px solid #999}
.cap{font-family:"Times New Roman",serif;font-size:15px;margin-bottom:6px}.c{text-align:center}.n{color:#a33;max-width:230px}
.f{font-size:12px;word-break:break-all}button{cursor:pointer}.box{background:#fff;border-left:5px solid #2e6b4b;padding:10px 16px;margin:12px 0}
.steps{font-size:14px;max-width:330px}.steps ol{margin:4px 0 6px 18px;padding:0}.hint{color:#555;font-size:12px;margin:4px 0}"""
JS = """function cp(id,b,label){var t=document.getElementById(id).innerText;var a=document.createElement("textarea");a.value=t;document.body.appendChild(a);a.select();try{document.execCommand("copy");b.innerText="Copied"}catch(e){b.innerText="Select and copy"}document.body.removeChild(a);setTimeout(function(){b.innerText=label},1200)}
var cs=document.querySelectorAll("input[type=checkbox]");for(var i=0;i<cs.length;i++){(function(c){try{c.checked=localStorage.getItem("done:"+c.dataset.k)=="1"}catch(e){}c.onchange=function(){try{localStorage.setItem("done:"+c.dataset.k,c.checked?"1":"0")}catch(e){}}})(cs[i])}"""


def table_row(entry, counter, with_steps):
    """One table row of the guide."""
    rel = entry["rel"].split("/", 1)[1]
    cap_id = "cap%d" % counter
    cells = ['<td class="c"><input type="checkbox" data-k="%s"></td>' % html.escape(entry["rel"]),
             "<td><b>%s</b></td>" % html.escape(entry["label"]),
             '<td><a href="%s" target="_blank"><img src="%s" alt="%s"></a></td>' % (
                 html.escape(rel), html.escape(rel), html.escape(entry["label"])),
             '<td><div class="cap" id="%s">%s</div><button onclick="cp(\'%s\',this,\'Copy caption\')">Copy caption</button></td>' % (
                 cap_id, html.escape(entry["label"] + ": " + entry["cap"]), cap_id)]
    if with_steps:
        steps = entry.get("steps") or []
        if steps:
            items = "".join("<li>%s</li>" % html.escape(text) for _n, text in steps)
            plain = "\n".join("%d. %s" % (n, text) for n, text in steps)
            cells.append('<td class="steps"><ol>%s</ol><div class="hint">The numbers on the picture match these steps.</div>'
                         '<div id="st%d" style="display:none">%s</div><button onclick="cp(\'st%d\',this,\'Copy steps\')">Copy steps</button></td>' % (
                             items, counter, html.escape(plain), counter))
        else:
            cells.append('<td class="steps">No steps: nothing to click on this picture.</td>')
    cells.append("<td>%s</td>" % html.escape(entry["sec"]))
    cells.append('<td class="f">%s<br><small>%s</small></td>' % (html.escape(rel.split("/")[-1]), entry["used"]))
    cells.append('<td class="n">%s</td>' % html.escape(entry["note"]))
    return "<tr>" + "".join(cells) + "</tr>"


def main():
    """Copy pictures, write the guides, zip, then report."""
    refused = move_old_outputs()
    os.makedirs(OUT)
    steps = read_steps()
    for entry in FIGURES:
        owner_folder = OWN[entry["o"]][0]
        number = entry["label"].split(" ")[1]
        if entry["kind"] == "MAN" and number != "54":
            source_path = os.path.join(ANN2, entry["src"])
            entry["used"] = "with numbered marks (Annotated_v2)"
            folder = "C3_User_manual_with_arrows"
        elif entry["kind"] == "MAN":
            source_path = os.path.join(SRC, entry["src"])
            entry["used"] = "plain"
            folder = "C3_User_manual_with_arrows"
        else:
            source_path = os.path.join(SRC, entry["src"])
            entry["used"] = "plain"
            folder = "A4_System_pages"
        match = re.match(r"(\d+)(.*)", number)
        file_name = "Fig_%02d%s_%s.png" % (int(match.group(1)), match.group(2), slug(entry["cap"]))
        target_dir = os.path.join(OUT, owner_folder, folder)
        os.makedirs(target_dir, exist_ok=True)
        target = os.path.join(target_dir, file_name)
        shutil.copy2(source_path, target)
        width, height = png_size(target)
        entry.update(rel=owner_folder + "/" + folder + "/" + file_name, source_path=source_path, w=width, h=height)
        if entry["kind"] == "MAN":
            entry["steps"] = steps.get(number, [])
        if width < 600:
            entry["note"] = (entry["note"] + " " if entry["note"] else "") + (
                "Small picture (%dx%d): only the pop-up box. Fine to paste; make it narrower in the doc." % (width, height))
    FIGURES.sort(key=lambda e: e["key"])

    counter = 0
    summary = []
    for owner, (folder, name, module, first) in OWN.items():
        mine = [e for e in FIGURES if e["o"] == owner]
        a4 = [e for e in mine if e["kind"] == "A4"]
        manual = [e for e in mine if e["kind"] == "MAN"]
        first_manual = manual[0]["label"].split(" ")[1] if manual else ""
        body = ["<h1>Hi %s, these are your pictures (%s)</h1>" % (html.escape(first), html.escape(module)),
                '<div class="box"><b>Your job: %d pictures</b> (%d for Section A.4 system GUI, %d for Section C.3 user manual).<ol>'
                "<li>Open the Google Doc and press Ctrl+F for the figure number (for example <i>Figure %s</i>).</li>"
                "<li>Delete the yellow <i>[Paste screenshot here]</i> line, then paste the picture: Insert &gt; Image &gt; "
                "Upload from computer, about 15 cm wide.</li>"
                "<li>Check the caption under it matches the one below (use Copy caption). Tick Done.</li></ol>"
                "<p>The user manual pictures have numbered red marks. The steps next to each picture use the same numbers: "
                "paste them under the picture (Copy steps).</p></div>" % (len(mine), len(a4), len(manual), first_manual)]
        for title, items, with_steps in (("Section A.4: System GUI screenshots", a4, False),
                                         ("Section C.3: User manual screenshots", manual, True)):
            rows = []
            for entry in items:
                counter += 1
                rows.append(table_row(entry, counter, with_steps))
            heads = ["Done", "Figure", "Picture (click to enlarge)", "Caption to type under it"]
            if with_steps:
                heads.append("Steps next to this picture")
            heads += ["Where in the report", "File", "Note"]
            body.append("<h2>%s (%d)</h2><table><tr>%s</tr>%s</table>" % (
                title, len(items), "".join("<th>%s</th>" % h for h in heads), "".join(rows)))
        page = ('<!DOCTYPE html><html><head><meta charset="utf-8"><title>%s: your screenshots</title><style>%s</style>'
                "</head><body>%s<script>%s</script></body></html>") % (html.escape(name), CSS, "".join(body), JS)
        with open(os.path.join(OUT, folder, "START_HERE.html"), "w", encoding="utf-8") as handle:
            handle.write(page)
        zip_path = os.path.join(OUT, folder + ".zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for root, _dirs, files in os.walk(os.path.join(OUT, folder)):
                for file_name in files:
                    full = os.path.join(root, file_name)
                    archive.write(full, os.path.join(folder, os.path.relpath(full, os.path.join(OUT, folder))))
        summary.append((folder, len(a4), len(manual), os.path.getsize(zip_path)))

    check(summary, refused)


def check(summary, refused):
    """Verify links, files, hashes, duplicates and print the table."""
    problems = []
    seen_hash_by_label = {}
    for entry in FIGURES:
        target = os.path.join(OUT, entry["rel"])
        if not os.path.isfile(target) or os.path.getsize(target) == 0:
            problems.append("missing " + entry["rel"])
            continue
        if sha(target) != sha(entry["source_path"]):
            problems.append("copy differs from its source: " + entry["rel"])
        if entry["kind"] == "MAN" and not entry["label"].endswith("54"):
            if not entry["source_path"].startswith(ANN2):
                problems.append("manual picture not from Annotated_v2: " + entry["rel"])
        seen_hash_by_label.setdefault(entry["label"], []).append(entry["o"])
    for label, owners in seen_hash_by_label.items():
        if len(owners) != 1:
            problems.append(f"{label} appears {len(owners)} times (owners {owners})")
    # every picture a guide refers to exists in that person's folder
    for owner, (folder, _n, _m, _f) in OWN.items():
        page = open(os.path.join(OUT, folder, "START_HERE.html"), encoding="utf-8").read()
        sources = re.findall(r'<img src="([^"]+)"', page)
        for source in sources:
            if not os.path.isfile(os.path.join(OUT, folder, html.unescape(source))):
                problems.append(f"{folder}: broken image link {source}")
        on_disk = []
        for root, _dirs, files in os.walk(os.path.join(OUT, folder)):
            for file_name in files:
                if file_name.endswith(".png"):
                    on_disk.append(os.path.relpath(os.path.join(root, file_name), os.path.join(OUT, folder)).replace("\\", "/"))
        if sorted(on_disk) != sorted(html.unescape(s) for s in sources):
            problems.append(f"{folder}: pictures on disk and in the guide differ")
        if "http://" in page.replace("</", "") and "src=\"http" in page:
            problems.append(f"{folder}: external link in guide")
    # a picture must not be in two people's folders (same file name or same hash twice)
    names = {}
    for entry in FIGURES:
        names.setdefault(os.path.basename(entry["rel"]), []).append(entry["o"])
    for name, owners in names.items():
        if len(owners) > 1:
            problems.append("same file name in several folders: " + name)
    # the zips hold only their own folder
    for folder, _a, _m, _s in summary:
        with zipfile.ZipFile(os.path.join(OUT, folder + ".zip")) as archive:
            for member in archive.namelist():
                if not member.startswith(folder + "/"):
                    problems.append(f"{folder}.zip contains {member}")
    expected = {"B": {"1", "2", "3", "4", "5", "6", "54", "55", "56", "57", "58", "59"},
                "M": {"7", "8", "8a", "8b", "9", "60", "61", "62", "63"},
                "C": {"10", "10a", "10b", "10c", "11", "11a", "11b", "11c", "12", "13", "14", "64", "65", "66", "67", "68", "69"},
                "L": {"15", "16", "17", "18", "19", "20", "70", "71", "72", "73", "74", "75"}}
    for owner, wanted in expected.items():
        got = {e["label"].split(" ")[1] for e in FIGURES if e["o"] == owner}
        if got != wanted:
            problems.append(f"{owner}: figures differ from the list (missing {sorted(wanted - got)}, extra {sorted(got - wanted)})")
    print()
    print(f"{'person folder':38} {'A.4':>4} {'C.3':>4} {'total':>5} {'zip':>10}")
    for folder, a4, manual, size in summary:
        print(f"{folder:38} {a4:>4} {manual:>4} {a4 + manual:>5} {size / 1024:>8.0f} KB")
    print("problems:", problems if problems else "none")
    if refused:
        print("NOT MOVED (delete these yourself):", refused)


if __name__ == "__main__":
    main()
