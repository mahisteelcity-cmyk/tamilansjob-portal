# TamilansJob.com - Tamil Nadu Government Job Portal

A comprehensive job portal website for Tamil Nadu government jobs and recruitment updates, built with Next.js, MongoDB, and TailwindCSS.

## 🎯 Features

### Core Functionality
- **Job Listings**: Browse latest government job opportunities
- **Advanced Filtering**: Filter by district, qualification, category, and search
- **Responsive Design**: Mobile-first, professional UI
- **Bilingual Support**: English and Tamil labels
- **Detailed Job Views**: Modal with overview, eligibility, and selection process

### Tamil Nadu Specific
- **Districts**: Chennai, Coimbatore, Madurai, Salem, Tirunelveli, Tiruchirappalli
- **Qualifications**: 10th, 12th/HSC, ITI, Diploma, B.E/B.Tech, B.Sc, Any Degree
- **Categories**: TNPSC, TRB, Police, Banking, Central Government, TN Government
- **Job Types**: Government, Education, Police, Central sectors

### Technical Features
- **Backend API**: RESTful endpoints with MongoDB
- **Real-time Search**: Instant filtering and pagination
- **SEO Optimized**: Meta tags, Open Graph, Twitter cards
- **Professional UI**: Clean government portal design

## 🛠️ Tech Stack

- **Frontend**: Next.js 14.2.3 (App Router), React 18
- **Backend**: Next.js API Routes, Node.js
- **Database**: MongoDB with UUID-based IDs
- **Styling**: TailwindCSS, shadcn/ui components
- **Icons**: Lucide React
- **Utils**: UUID, date-fns, axios

## 📦 Installation

### Prerequisites
- Node.js 18+ 
- MongoDB (local or cloud)
- Yarn package manager

### Setup Steps

1. **Clone/Extract Project**
```bash
# Extract the project files to your desired directory
cd your-project-directory
```

2. **Install Dependencies**
```bash
yarn install
```

3. **Environment Variables**
Create `.env` file in root directory:
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=tamilansjob_db
NEXT_PUBLIC_BASE_URL=http://localhost:3000
CORS_ORIGINS=*
```

4. **Start MongoDB**
```bash
# For local MongoDB
mongod

# Or use MongoDB Atlas cloud connection
# Update MONGO_URL with your Atlas connection string
```

5. **Run Development Server**
```bash
yarn dev
```

6. **Access Application**
- Frontend: http://localhost:3000
- API: http://localhost:3000/api

## 🗄️ Database Schema

### Collections

#### Districts
```javascript
{
  id: "uuid",
  name_en: "Chennai",
  name_ta: "சென்னை", 
  slug: "chennai",
  createdAt: Date
}
```

#### Qualifications
```javascript
{
  id: "uuid",
  name_en: "B.E/B.Tech",
  name_ta: "பி.இ/பி.டெக்",
  slug: "be-btech",
  order: 5,
  createdAt: Date
}
```

#### Categories
```javascript
{
  id: "uuid",
  name_en: "TNPSC",
  name_ta: "தமிழ்நாடு பொதுப்பணி ஆணையம்",
  slug: "tnpsc",
  sector: "government",
  parentId: null,
  createdAt: Date
}
```

#### Jobs
```javascript
{
  id: "uuid",
  title: "TNPSC Group 4 Recruitment 2025",
  slug: "tnpsc-group-4-recruitment-2025",
  summary: "Brief description",
  content: "Full description",
  vacancies: 1958,
  dept: "Tamil Nadu Public Service Commission",
  sector: "government",
  board: "TNPSC",
  jobType: "permanent",
  payScale: "₹19,500 - ₹62,000",
  salaryFrom: 19500,
  salaryTo: 62000,
  ageMin: 18,
  ageMax: 30,
  fees: 150,
  selectionProcess: "Written Exam + Interview",
  mode: "online",
  lastDate: Date,
  postDate: Date,
  districtId: "district-uuid",
  qualificationIds: ["qual-uuid"],
  categoryIds: ["category-uuid"],
  tags: ["group4", "government"],
  notifyPdfUrl: "https://example.com/notification.pdf",
  applyUrl: "https://tnpsc.gov.in",
  sourceUrl: "https://tnpsc.gov.in",
  status: "published",
  lang: "en",
  createdAt: Date,
  updatedAt: Date
}
```

## 🔌 API Endpoints

### Seed Data
- `POST /api/seed` - Initialize database with sample data

### Districts
- `GET /api/districts` - Get all districts
- `POST /api/districts` - Create new district

### Qualifications  
- `GET /api/qualifications` - Get all qualifications
- `POST /api/qualifications` - Create new qualification

### Categories
- `GET /api/categories` - Get all categories
- `POST /api/categories` - Create new category

### Jobs
- `GET /api/jobs` - Get jobs with filtering
- `GET /api/jobs?district=ID&qualification=ID&category=ID&search=term&page=1&limit=10`
- `POST /api/jobs` - Create new job
- `GET /api/jobs/{job-id}` - Get single job

### Query Parameters for Jobs
- `district`: Filter by district ID
- `qualification`: Filter by qualification ID  
- `category`: Filter by category ID
- `search`: Search in title, department, summary
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)

## 🚀 Deployment

### Production Build
```bash
yarn build
yarn start
```

### Environment Variables (Production)
```env
MONGO_URL=mongodb://your-production-mongodb-url
DB_NAME=tamilansjob_production
NEXT_PUBLIC_BASE_URL=https://tamilansjob.com
CORS_ORIGINS=https://tamilansjob.com
```

### Deployment Platforms
- **Vercel**: Connect GitHub repo, auto-deploy
- **Netlify**: Build command: `yarn build`, Publish: `.next`
- **VPS/Cloud**: PM2, Docker, or direct Node.js

## 🎨 UI Components

The application uses shadcn/ui components:
- `Button` - Primary actions and links
- `Card` - Job listings and containers  
- `Input` - Search and form fields
- `Select` - Filter dropdowns
- `Badge` - Tags and status indicators
- `Dialog` - Job detail modals
- `Tabs` - Job detail sections

## 📱 Mobile Support

- Responsive design for all screen sizes
- Touch-friendly interface
- Optimized for mobile job searching
- Fast loading on mobile networks

## 🔍 SEO Features

- Semantic HTML structure
- Meta tags for social sharing
- Open Graph and Twitter cards
- Structured data for job postings
- Clean URLs with slugs

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check MongoDB is running
   - Verify MONGO_URL in .env file
   - Check network connectivity

2. **API Routes Not Working**
   - Ensure API calls use `/api` prefix
   - Check CORS configuration
   - Verify route file structure

3. **Build Errors**
   - Clear `.next` folder: `rm -rf .next`
   - Clear node_modules: `rm -rf node_modules && yarn install`
   - Check Node.js version (18+)

4. **Styling Issues**
   - Verify Tailwind CSS configuration
   - Check shadcn/ui component imports
   - Clear browser cache

## 📄 License

This project is created for TamilansJob.com. All rights reserved.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly  
5. Submit pull request

## 📞 Support

For technical support or feature requests, please create an issue in the repository.

---

**TamilansJob.com** - Your gateway to Tamil Nadu government job opportunities! 🏛️🎯