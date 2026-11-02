"""Creates a synthetic dataset: data/jobs.csv  (label 1 = fraud, 0 = genuine)."""
import random, pandas as pd
random.seed(42)

roles = ["Software Engineer", "Data Analyst", "HR Executive", "Sales Manager", "Accountant",
         "Content Writer", "Customer Support Associate", "Business Analyst", "Python Developer", "Digital Marketer"]
companies = ["Infosys", "TCS", "Wipro", "Zoho", "Accenture", "Cognizant", "HCLTech", "Capgemini", "Tech Mahindra", "Deloitte"]
cities = ["Hyderabad", "Bengaluru", "Pune", "Chennai", "Mumbai", "Noida"]

def genuine():
    r, c, city = random.choice(roles), random.choice(companies), random.choice(cities)
    text = (f"{c} is hiring a {r} for our {city} office. Responsibilities include working with cross-functional teams, "
            f"delivering quality work and meeting project timelines. Requirements: {random.randint(1,6)}+ years of relevant experience, "
            f"a bachelor's degree and good communication skills. The selection process includes a technical interview and an HR round. "
            f"Benefits: health insurance, provident fund and paid leave. Apply through our official careers page at careers.{c.lower().replace(' ','')}.com. "
            f"Contact: hr@{c.lower().replace(' ','')}.com")
    if random.random() < 0.15:   # genuine posts can also sound urgent or use WhatsApp
        text += random.choice([" Urgent opening, join immediately.", " Join our WhatsApp group for updates.", " Reach us at recruiter@gmail.com for queries."])
    return r, c, text, 0

def fraud():
    r, c = random.choice(roles), random.choice(companies)
    parts = [
        f"URGENT hiring for {r}! Work from home, earn Rs {random.choice([2000,3000,5000,8000])} per day. No interview, direct joining.",
        "No experience required, only 10 minutes daily work. Guaranteed income every week.",
        f"Pay a refundable registration fee of Rs {random.choice([500,999,1500,2500])} to confirm your seat. Limited seats, apply immediately.",
        f"Send your resume and Aadhaar copy on WhatsApp +91 9{random.randint(100000000,999999999)}.",
        f"Contact: {c.lower().replace(' ','')}.hr.jobs{random.randint(1,99)}@gmail.com",
        "Pay a security deposit for laptop kit, it will be returned after first salary.",
        "Selection is 100% guaranteed. Message us on Telegram now.",
    ]
    random.shuffle(parts)
    text = " ".join(parts[:random.randint(3, 6)])
    if random.random() < 0.4:   # some scams copy real company language to look legit
        text = f"{c} is hiring a {r}. " + text
    if random.random() < 0.2:    # subtle scams: polished text, only one or two flags
        text = (f"{c} is hiring a {r}. Responsibilities include data entry and coordination. "
                f"Requirements: any graduate. Selection is online, kindly pay a small processing fee after shortlisting. "
                f"Contact: {c.lower()}jobs@gmail.com")
    return r, c, text, 1

rows = [genuine() for _ in range(450)] + [fraud() for _ in range(300)]
random.shuffle(rows)
pd.DataFrame(rows, columns=["title", "company", "description", "fraudulent"]).to_csv("data/jobs.csv", index=False)
print("Saved data/jobs.csv with", len(rows), "rows")
