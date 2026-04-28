import React from 'react'
import { AuthProvider, useAuth } from './context/AuthContext'
import { protectedPaths, routes } from './constants/routes'
import { useRouter } from './hooks/useRouter'
import Footer from './layout/Footer'
import Navbar from './layout/Navbar'
import Sidebar from './layout/Sidebar'
import ProtectedRoute from './components/ProtectedRoute'
import {
  AdminDashboardPage,
  ConsultantDashboardPage,
  DashboardPage,
  DocumentChecklistPage,
  DocumentsPage,
  HomePage,
  JobRelocationPage,
  LoginPage,
  NotFoundPage,
  PaymentFailedPage,
  PaymentPage,
  PaymentSuccessPage,
  PricingPage,
  ProfilePage,
  RefusalAnalysisPage,
  RegisterPage,
  SopGeneratorPage,
  StudyPlacementPage,
  VisaAssessmentPage,
} from './pages/pages'

function AppShell() {
  const { path, navigate } = useRouter()
  const { isAuthenticated } = useAuth()

  const pages = {
    [routes.home]: <HomePage navigate={navigate} />,
    [routes.login]: <LoginPage navigate={navigate} />,
    [routes.register]: <RegisterPage navigate={navigate} />,
    [routes.dashboard]: <DashboardPage navigate={navigate} />,
    [routes.visaAssessment]: <VisaAssessmentPage />,
    [routes.documentChecklist]: <DocumentChecklistPage />,
    [routes.documents]: <DocumentsPage />,
    [routes.sopGenerator]: <SopGeneratorPage />,
    [routes.refusalAnalysis]: <RefusalAnalysisPage />,
    [routes.studyPlacement]: <StudyPlacementPage />,
    [routes.jobRelocation]: <JobRelocationPage />,
    [routes.pricing]: <PricingPage navigate={navigate} />,
    [routes.payment]: <PaymentPage navigate={navigate} />,
    [routes.paymentCallback]: <PaymentSuccessPage navigate={navigate} />,
    [routes.paymentSuccess]: <PaymentSuccessPage navigate={navigate} />,
    [routes.paymentFailed]: <PaymentFailedPage />,
    [routes.profile]: <ProfilePage />,
    [routes.consultantDashboard]: <ConsultantDashboardPage />,
    [routes.adminDashboard]: <AdminDashboardPage />,
  }

  const content = pages[path] || <NotFoundPage />
  const shouldProtect = protectedPaths.has(path)

  return (
    <main className="app-shell">
      <Navbar navigate={navigate} />
      <div className="app-body">
        {isAuthenticated ? <Sidebar navigate={navigate} /> : null}
        <section className="content">
          {shouldProtect ? <ProtectedRoute navigate={navigate}>{content}</ProtectedRoute> : content}
        </section>
      </div>
    <Footer />
    </main>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <AppShell />
    </AuthProvider>
  )
}