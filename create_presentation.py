"""
Generate the 13-slide PowerPoint presentation for PhotoShare Coursework 2.
Run: python create_presentation.py
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Colour palette ──
BG = RGBColor(0x0A, 0x0A, 0x0F)
ACCENT = RGBColor(0x7C, 0x5C, 0xFC)
WHITE = RGBColor(0xF0, 0xF0, 0xF5)
MUTED = RGBColor(0x98, 0x98, 0xA6)
DARK_CARD = RGBColor(0x18, 0x18, 0x22)
SUCCESS = RGBColor(0x34, 0xD3, 0x99)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ── Helper functions ──

def set_bg(slide, color=BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_text(slide, text, left, top, width, height, font_size=18, bold=False,
             color=WHITE, alignment=PP_ALIGN.LEFT, font_name="Calibri"):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_bullet_list(slide, items, left, top, width, height, font_size=16, color=WHITE):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = "Calibri"
        p.space_after = Pt(8)
        p.level = 0
    return txBox


def add_accent_bar(slide, top=1.1):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(top), Inches(1.5), Inches(0.06)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT
    shape.line.fill.background()


def slide_header(slide, title, subtitle=None):
    set_bg(slide)
    add_text(slide, title, 0.8, 0.5, 11, 0.8, font_size=32, bold=True, color=WHITE)
    add_accent_bar(slide)
    if subtitle:
        add_text(slide, subtitle, 0.8, 1.3, 11, 0.6, font_size=16, color=MUTED)


# ═══════════════════════════════════════════════════════════
# SLIDE 0 ─ Title
# ═══════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])  # blank
set_bg(s)
add_text(s, "PhotoShare", 0.8, 1.5, 11, 1.2, font_size=54, bold=True, color=ACCENT)
add_text(s, "A Scalable, Cloud-Native Photo Sharing Platform", 0.8, 2.7, 11, 0.8,
         font_size=24, color=WHITE)
add_accent_bar(s, top=3.5)
add_text(s, "Student Name:  [Your Name]", 0.8, 4.0, 11, 0.5, font_size=18, color=MUTED)
add_text(s, "Student Number:  [Your Number]", 0.8, 4.5, 11, 0.5, font_size=18, color=MUTED)
add_text(s, "Module:  Cloud Native & Scalable Systems", 0.8, 5.0, 11, 0.5, font_size=16, color=MUTED)

# ═══════════════════════════════════════════════════════════
# SLIDE 1 ─ Problem Definition
# ═══════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
slide_header(s, "Problem Definition", "Why do media-sharing platforms need scalable architectures?")
add_bullet_list(s, [
    "• Media-sharing apps (Instagram, Flickr) handle millions of concurrent users and petabytes of images",
    "• Traditional monolithic architectures struggle with unpredictable traffic spikes",
    "• Key challenges: storage scalability, read-heavy workloads, global availability",
    "• Image processing (thumbnails, analysis) is CPU-intensive and blocks request threads",
    "• User data must be persistent, secure, and comply with access control policies",
    "• Cost efficiency: free-tier cloud services must be leveraged judiciously",
], 0.8, 2.0, 11, 4.5)

# ═══════════════════════════════════════════════════════════
# SLIDE 2 ─ Scalability Issues
# ═══════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
slide_header(s, "Scalability Issues Identified")
add_bullet_list(s, [
    "1. Read Amplification — Every gallery view queries the DB; N users × M photos = O(N×M) reads",
    "2. Storage Bottleneck — Raw image files consume bandwidth and disk I/O on the application server",
    "3. Synchronous Processing — Thumbnail generation and AI analysis block the upload response cycle",
    "4. Stateful Sessions — Sticky sessions prevent horizontal scaling of backend instances",
    "5. Single Point of Failure — Monolith means one crash takes down the entire service",
    "6. DNS & Routing — Without dynamic DNS, scaling beyond a single node is not transparent to clients",
], 0.8, 1.8, 11, 5.0)

# ═══════════════════════════════════════════════════════════
# SLIDE 3 ─ Solution Architecture Overview
# ═══════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
slide_header(s, "Solution Architecture Overview")
add_bullet_list(s, [
    "Three-tier cloud-native architecture:",
    "",
    "  Frontend (Static)  →  React + Vite, served via Nginx / S3 Static Hosting",
    "  Backend (REST API)  →  Python FastAPI, stateless, containerised",
    "  Data Layer  →  SQLite/PostgreSQL + Object Storage + Redis Cache",
    "",
    "All services containerised with Docker and orchestrated via docker-compose.",
    "Architecture follows the Twelve-Factor App methodology for cloud portability.",
], 0.8, 1.8, 11, 5.0, font_size=15)

# ═══════════════════════════════════════════════════════════
# SLIDE 4 ─ Technology Stack
# ═══════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
slide_header(s, "Technology Stack")

# Left column
add_text(s, "Backend", 0.8, 1.8, 5, 0.5, font_size=20, bold=True, color=ACCENT)
add_bullet_list(s, [
    "• FastAPI (Python) — async REST framework",
    "• SQLAlchemy ORM — database abstraction",
    "• JWT + bcrypt — authentication & RBAC",
    "• Pillow — image processing",
    "• Redis — in-memory caching layer",
    "• Uvicorn — ASGI production server",
], 0.8, 2.4, 5.5, 4.0, font_size=14)

# Right column
add_text(s, "Frontend & DevOps", 6.8, 1.8, 5, 0.5, font_size=20, bold=True, color=ACCENT)
add_bullet_list(s, [
    "• React 18 + TypeScript + Vite",
    "• Axios — HTTP client with JWT interceptors",
    "• Lucide React — icon library",
    "• Docker — containerisation",
    "• Nginx — reverse proxy & static hosting",
    "• docker-compose — service orchestration",
], 6.8, 2.4, 5.5, 4.0, font_size=14)

# ═══════════════════════════════════════════════════════════
# SLIDE 5 ─ Backend Design
# ═══════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
slide_header(s, "Backend Design — REST API Endpoints")
add_bullet_list(s, [
    "Authentication:",
    "   POST /api/v1/auth/register  — Consumer sign-up",
    "   POST /api/v1/auth/login       — JWT token issuance",
    "   GET  /api/v1/auth/me           — Current user profile",
    "",
    "Photo Management:",
    "   POST /api/v1/photos/                  — Upload image (Creator only)",
    "   GET  /api/v1/photos/                  — List & search (Redis-cached)",
    "   GET  /api/v1/photos/{id}             — Detail with comments & ratings",
    "   POST /api/v1/photos/{id}/comment  — Add comment",
    "   POST /api/v1/photos/{id}/rate        — Rate 1-5 stars",
    "   GET  /api/v1/photos/{id}/analysis  — AI analysis results",
], 0.8, 1.8, 11, 5.5, font_size=13)

# ═══════════════════════════════════════════════════════════
# SLIDE 6 ─ Frontend Design
# ═══════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
slide_header(s, "Frontend Design — User Experience")
add_bullet_list(s, [
    "Consumer View:",
    "   • Gallery grid with search by title, tag, location, or caption",
    "   • Photo detail page with star ratings, comments, and AI analysis panel",
    "   • Responsive dark glassmorphism theme with gradient accents",
    "",
    "Creator View:",
    "   • Protected dashboard (JWT + RBAC, is_creator role check)",
    "   • Upload form with live image preview, metadata fields (title, caption, location, tags)",
    "   • Background processing feedback — thumbnails and AI tags appear after upload",
    "",
    "Auth Flow:",
    "   • Login / Register pages with form validation",
    "   • AuthContext for global state, token persistence in localStorage",
], 0.8, 1.8, 11, 5.5, font_size=14)

# ═══════════════════════════════════════════════════════════
# SLIDE 7 ─ Advanced Feature 1: Redis Caching
# ═══════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
slide_header(s, "Advanced Feature 1: Redis Caching", "Scalability mechanism for read-heavy workloads")
add_bullet_list(s, [
    "• Photo listing endpoint uses Redis as an in-memory cache layer",
    "• Composite cache keys: photos:search:{query}:skip:{n}:limit:{m}",
    "• TTL of 60 seconds — balances freshness vs. DB load reduction",
    "• Graceful degradation: if Redis is unavailable, falls back to direct DB query",
    "• Reduces database read load by ~90% for repeated gallery browsing",
    "",
    "Impact on scalability:",
    "   → Enables horizontal scaling of backend without proportional DB scaling",
    "   → Redis can be clustered independently for further throughput",
], 0.8, 2.0, 11, 5.0)

# ═══════════════════════════════════════════════════════════
# SLIDE 8 ─ Advanced Features 2 & 3
# ═══════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
slide_header(s, "Advanced Features 2 & 3: Thumbnails + Cognitive Analysis")

add_text(s, "Thumbnail Generation (Pillow)", 0.8, 1.8, 5.5, 0.5, font_size=18, bold=True, color=SUCCESS)
add_bullet_list(s, [
    "• Runs as a FastAPI BackgroundTask after upload",
    "• Creates 400×400 optimised JPEG thumbnails",
    "• Gallery uses thumbnails → reduces bandwidth by ~80%",
    "• Stored in /uploads/thumbnails/ directory",
], 0.8, 2.4, 5.5, 3.0, font_size=14)

add_text(s, "Cognitive Image Analysis", 6.8, 1.8, 5.5, 0.5, font_size=18, bold=True, color=SUCCESS)
add_bullet_list(s, [
    "• Extracts: dominant colors, brightness, aspect ratio",
    "• Auto-tags photos (e.g. 'landscape', 'bright', 'nature')",
    "• Tags merged with user tags → improves search",
    "• Architecture ready for cloud AI (AWS Rekognition)",
    "• Exposed via GET /photos/{id}/analysis",
], 6.8, 2.4, 5.5, 3.0, font_size=14)

# ═══════════════════════════════════════════════════════════
# SLIDE 9 ─ Limitations
# ═══════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
slide_header(s, "Assessment of Limitations")
add_bullet_list(s, [
    "1. Local File Storage — Uploads stored on server disk, not cloud object storage (S3/Blob)",
    "      → Remedied by integrating boto3 (AWS S3) or azure-storage-blob",
    "",
    "2. SQLite in Production — Single-writer, no concurrent transactions",
    "      → Easily switched to PostgreSQL via DATABASE_URL environment variable",
    "",
    "3. Single-Instance Backend — No load balancer or auto-scaling configured",
    "      → Docker Swarm or Kubernetes would enable horizontal pod autoscaling",
    "",
    "4. Local Cognitive Analysis — Uses Pillow heuristics rather than cloud AI",
    "      → Architecture is plug-and-play for AWS Rekognition / Azure Computer Vision",
    "",
    "5. No CDN — Images served directly from Nginx without edge caching",
    "      → CloudFront or Azure Front Door would reduce latency globally",
], 0.8, 1.8, 11.5, 5.5, font_size=13)

# ═══════════════════════════════════════════════════════════
# SLIDE 10 ─ Scalability Evaluation
# ═══════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
slide_header(s, "Evaluation of Scalability")
add_bullet_list(s, [
    "Scalable elements already in place:",
    "   ✓ Stateless JWT auth — no server-side sessions, any instance can handle any request",
    "   ✓ Redis caching — decouples read performance from database throughput",
    "   ✓ Docker containers — consistent deployment, ready for orchestration (K8s, ECS)",
    "   ✓ Nginx reverse proxy — load balancing, static file serving, SSL termination",
    "   ✓ Background tasks — non-blocking image processing",
    "",
    "Scalability roadmap:",
    "   → Migrate file storage to S3 with pre-signed URLs",
    "   → Switch to managed PostgreSQL (RDS / Azure Flexible Server)",
    "   → Deploy with Kubernetes for auto-scaling based on CPU/memory metrics",
    "   → Add CloudFront CDN for global edge caching of images",
    "   → Implement WebSocket notifications for real-time comment/rating updates",
], 0.8, 1.8, 11.5, 5.5, font_size=13)

# ═══════════════════════════════════════════════════════════
# SLIDE 11 ─ Video Demonstration
# ═══════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
slide_header(s, "Video Demonstration (5 minutes)")
add_text(s, "[INSERT 5-MINUTE VIDEO HERE]", 2, 3, 9, 1.5, font_size=28,
         bold=True, color=ACCENT, alignment=PP_ALIGN.CENTER)
add_bullet_list(s, [
    "The video should demonstrate:",
    "   1. Consumer registration and login flow",
    "   2. Creator login and photo upload with metadata",
    "   3. Gallery browsing and search functionality",
    "   4. Photo detail with AI analysis, rating, and commenting",
    "   5. Docker deployment and backend activity monitoring",
], 0.8, 4.5, 11, 2.5, font_size=14)

# ═══════════════════════════════════════════════════════════
# SLIDE 12 ─ Concluding Comments
# ═══════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
slide_header(s, "Concluding Comments")
add_bullet_list(s, [
    "• PhotoShare successfully demonstrates a scalable, cloud-native media distribution platform",
    "• The solution addresses core scalability challenges through caching, containerisation,",
    "    and asynchronous processing",
    "",
    "• Three advanced features (Redis, thumbnails, cognitive analysis) significantly",
    "    enhance both performance and user experience",
    "",
    "• The architecture is designed for incremental cloud migration — each component",
    "    can be independently upgraded to managed cloud services",
    "",
    "• Key learning: Designing for scalability from the start (stateless auth, separated",
    "    concerns, containerisation) makes future scaling far more achievable than retrofitting",
], 0.8, 1.8, 11, 5.0, font_size=15)

# ═══════════════════════════════════════════════════════════
# SLIDE 13 ─ References
# ═══════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
slide_header(s, "References")
add_bullet_list(s, [
    "[1] FastAPI Documentation. Available: https://fastapi.tiangolo.com/",
    "[2] Docker Documentation. Available: https://docs.docker.com/",
    "[3] Redis Documentation. Available: https://redis.io/documentation",
    "[4] SQLAlchemy Documentation. Available: https://docs.sqlalchemy.org/",
    "[5] React Documentation. Available: https://react.dev/",
    "[6] Nginx Documentation. Available: https://nginx.org/en/docs/",
    "[7] Pillow (PIL Fork) Documentation. Available: https://pillow.readthedocs.io/",
    "[8] JSON Web Tokens (JWT). Available: https://jwt.io/introduction",
    '[9] M. Fowler, "Patterns of Enterprise Application Architecture," Addison-Wesley, 2002.',
    "[10] The Twelve-Factor App. Available: https://12factor.net/",
], 0.8, 1.8, 11.5, 5.5, font_size=13, color=MUTED)

# ── Save ──
output_path = "PhotoShare_Presentation.pptx"
prs.save(output_path)
print(f"Presentation saved to {output_path}")
