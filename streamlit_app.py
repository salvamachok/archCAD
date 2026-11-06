import json
from datetime import date

import streamlit as st

st.set_page_config(
    page_title="archCAD | Architectural Studio",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- DESIGN --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: #f5f6f8;
}
section[data-testid="stSidebar"] {
    background: #171a21;
}
section[data-testid="stSidebar"] * {
    color: #f5f6f8 !important;
}
.brand {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #18212f;
}
.subtitle {
    color: #7b8492;
    margin-bottom: 25px;
}
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 13px;
    border: 1px solid #e5e8ed;
}
.metric-label {
    color: #818a98;
    font-size: 12px;
    text-transform: uppercase;
}
.metric-value {
    color: #172333;
    font-size: 25px;
    font-weight: 800;
    margin-top: 5px;
}
.section-card {
    background: white;
    border: 1px solid #e5e8ed;
    padding: 20px;
    border-radius: 13px;
    margin-bottom: 15px;
}
h1, h2, h3 {
    color: #172333;
}
.stButton button {
    border-radius: 8px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# -------------------- SESSION DATA --------------------

if "project" not in st.session_state:
    st.session_state.project = {
        "name": "My Architectural Project",
        "type": "Residential",
        "location": "",
        "site_area": 1000.0,
        "floors": 1,
        "climate": "Tropical",
        "client": "",
        "description": "",
        "spaces": [
            {"name": "Living Room", "area": 30.0, "quantity": 1},
            {"name": "Kitchen", "area": 15.0, "quantity": 1},
            {"name": "Bedroom", "area": 16.0, "quantity": 3},
            {"name": "Bathroom", "area": 6.0, "quantity": 2},
            {"name": "Dining Room", "area": 18.0, "quantity": 1}
        ]
    }

p = st.session_state.project

# -------------------- HELPERS --------------------

def total_area():
    return sum(
        s["area"] * s["quantity"]
        for s in p["spaces"]
    )

def project_score():
    score = 100
    if not p["name"].strip():
        score -= 15
    if not p["location"].strip():
        score -= 10
    if p["site_area"] <= 0:
        score -= 25
    if not p["spaces"]:
        score -= 30
    if total_area() > p["site_area"] * p["floors"]:
        score -= 20
    return max(0, score)

def export_data():
    return json.dumps(p, indent=4)

# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown("# archCAD")
    st.caption("ARCHITECTURAL DESIGN STUDIO")
    st.divider()

    page = st.radio(
        "WORKSPACE",
        [
            "Dashboard",
            "Project Brief",
            "Space Programme",
            "Site Planning",
            "Design Review",
            "Project Report"
        ]
    )

    st.divider()
    st.caption("PROJECT")
    st.write(p["name"])
    st.caption(f'{p["type"]} | {p["floors"]} floor(s)')

    st.divider()
    st.caption("archCAD Conceptual Planning Environment")

# -------------------- HEADER --------------------

st.markdown('<div class="brand">archCAD</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Architectural planning and design workspace</div>',
    unsafe_allow_html=True
)

# -------------------- DASHBOARD --------------------

if page == "Dashboard":

    st.title("Project Dashboard")
    st.write("Overview of your architectural project.")

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("SITE AREA", f'{p["site_area"]:,.0f} m²'),
        ("PROGRAMMED AREA", f'{total_area():,.1f} m²'),
        ("FLOORS", str(p["floors"])),
        ("DESIGN SCORE", f'{project_score()}%')
    ]

    for col, (label, value) in zip([c1,c2,c3,c4], metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    left, right = st.columns([1.4, 1])

    with left:
        st.subheader("Project Information")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.write("**Project:**", p["name"])
        st.write("**Building type:**", p["type"])
        st.write("**Location:**", p["location"] or "Not specified")
        st.write("**Client:**", p["client"] or "Not specified")
        st.write("**Climate:**", p["climate"])
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.subheader("Design Progress")
        st.progress(project_score() / 100)
        st.write(f"Current score: {project_score()}%")
        st.caption("Preliminary completeness indicator, not regulatory certification.")

        if total_area() > p["site_area"] * p["floors"]:
            st.warning("Programmed area exceeds the available site-area allowance.")

    st.subheader("Space Programme")
    if p["spaces"]:
        st.dataframe(p["spaces"], use_container_width=True)
    else:
        st.info("No spaces have been added yet.")

# -------------------- PROJECT BRIEF --------------------

elif page == "Project Brief":

    st.title("Project Brief")
    st.write("Define the basic requirements of your building.")

    with st.form("project_form"):
        name = st.text_input("Project name", p["name"])
        building_type = st.selectbox(
            "Building type",
            [
                "Residential", "Commercial", "Office",
                "Educational", "Healthcare", "Industrial",
                "Hospitality", "Mixed Use", "Institutional"
            ],
            index=[
                "Residential", "Commercial", "Office",
                "Educational", "Healthcare", "Industrial",
                "Hospitality", "Mixed Use", "Institutional"
            ].index(p["type"])
            if p["type"] in [
                "Residential", "Commercial", "Office",
                "Educational", "Healthcare", "Industrial",
                "Hospitality", "Mixed Use", "Institutional"
            ] else 0
        )

        client = st.text_input("Client", p["client"])
        location = st.text_input("Project location", p["location"])
        site_area = st.number_input(
            "Site area (m²)", min_value=1.0,
            value=float(p["site_area"])
        )
        floors = st.number_input(
            "Number of floors", min_value=1,
            max_value=100, value=int(p["floors"])
        )
        climate = st.selectbox(
            "Climate",
            ["Tropical", "Temperate", "Arid", "Cold", "Mediterranean"],
            index=["Tropical", "Temperate", "Arid", "Cold", "Mediterranean"].index(p["climate"])
        )
        description = st.text_area(
            "Project description", p["description"]
        )

        submitted = st.form_submit_button(
            "Save Project Brief",
            type="primary",
            use_container_width=True
        )

        if submitted:
            p.update({
                "name": name,
                "type": building_type,
                "client": client,
                "location": location,
                "site_area": site_area,
                "floors": floors,
                "climate": climate,
                "description": description
            })
            st.success("Project brief saved.")
            st.rerun()

# -------------------- SPACE PROGRAMME --------------------

elif page == "Space Programme":

    st.title("Space Programme")
    st.write("Create and manage building spaces.")

    with st.form("space_form"):
        name = st.text_input("Space name")
        area = st.number_input(
            "Area per space (m²)",
            min_value=0.1,
            value=15.0
        )
        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1
        )

        add = st.form_submit_button(
            "Add Space",
            type="primary"
        )

        if add:
            if name.strip():
                p["spaces"].append({
                    "name": name.strip(),
                    "area": float(area),
                    "quantity": int(quantity)
                })
                st.success("Space added.")
                st.rerun()
            else:
                st.error("Enter a space name.")

    st.divider()
    st.subheader("Current Spaces")

    if p["spaces"]:
        for i, space in enumerate(p["spaces"]):
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            c1.write(space["name"])
            c2.write(f'{space["area"]} m²')
            c3.write(f'× {space["quantity"]}')
            if c4.button("Remove", key=f"remove_{i}"):
                p["spaces"].pop(i)
                st.rerun()

    st.divider()
    st.metric("Total programmed area", f"{total_area():,.1f} m²")

# -------------------- SITE PLANNING --------------------

elif page == "Site Planning":

    st.title("Site Planning")
    st.write("Review preliminary site and building area relationships.")

    coverage = total_area() / p["site_area"] * 100
    floor_area_ratio = total_area() / p["site_area"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Site area", f'{p["site_area"]:,.1f} m²')
    c2.metric("Programmed area", f'{total_area():,.1f} m²')
    c3.metric("Area / site ratio", f"{floor_area_ratio:.2f}")

    st.subheader("Preliminary Area Assessment")
    st.write(f"Programmed area divided by site area: {coverage:.1f}%")

    st.progress(min(coverage / 100, 1.0))

    if coverage > 100:
        st.warning("Programmed area exceeds the site area. Check building layout and floor distribution.")
    else:
        st.success("Programmed area is within the total site-area figure.")

    st.info(
        "These are preliminary arithmetic checks. Actual site coverage, "
        "setbacks, floor-area ratio, parking and building height must be "
        "checked against local planning regulations."
    )

# -------------------- DESIGN REVIEW --------------------

elif page == "Design Review":

    st.title("Design Review")
    st.write("Preliminary project completeness and area checks.")

    score = project_score()
    st.metric("Project completeness score", f"{score}%")
    st.progress(score / 100)

    checks = {
        "Project name defined": bool(p["name"].strip()),
        "Building type selected": bool(p["type"]),
        "Project location defined": bool(p["location"].strip()),
        "Site area provided": p["site_area"] > 0,
        "At least one space programmed": len(p["spaces"]) > 0,
        "Programmed area within site-area figure": total_area() <= p["site_area"] * p["floors"]
    }

    for label, passed in checks.items():
        if passed:
            st.success(label)
        else:
            st.warning(label)

    st.caption(
        "This score measures basic data completeness only. It is not "
        "a structural, architectural, safety or code-compliance approval."
    )

# -------------------- REPORT --------------------

elif page == "Project Report":

    st.title("Project Report")

    st.subheader(p["name"])
    st.write(f"**Date:** {date.today().isoformat()}")
    st.write(f'**Building type:** {p["type"]}')
    st.write(f'**Location:** {p["location"] or "Not specified"}')
    st.write(f'**Site area:** {p["site_area"]:,.1f} m²')
    st.write(f'**Floors:** {p["floors"]}')
    st.write(f'**Climate:** {p["climate"]}')
    st.write(f'**Programmed area:** {total_area():,.1f} m²')

    st.subheader("Space Schedule")
    if p["spaces"]:
        st.dataframe(p["spaces"], use_container_width=True)

    st.subheader("Project Description")
    st.write(p["description"] or "No description provided.")

    st.download_button(
        "Download Project JSON",
        data=export_data(),
        file_name="archcad_project.json",
        mime="application/json",
        use_container_width=True
    )

    st.download_button(
        "Download Space Schedule CSV",
        data=__import__("pandas").DataFrame(p["spaces"]).to_csv(index=False),
        file_name="archcad_space_schedule.csv",
        mime="text/csv",
        use_container_width=True
    )

# -------------------- FOOTER --------------------

st.divider()
st.caption(
    "archCAD | Architectural Design Studio | "
    "Conceptual planning tool. Verify all professional and statutory requirements."
)