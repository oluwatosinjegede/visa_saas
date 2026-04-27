import React, { useMemo, useState } from 'react'
import AlertMessage from '../components/AlertMessage'
import DashboardCard from '../components/DashboardCard'
import FormInput from '../components/FormInput'
import LoadingSpinner from '../components/LoadingSpinner'
import PlanCard from '../components/PlanCard'
import ServiceCard from '../components/ServiceCard'
import { useAuth } from '../context/AuthContext'
import { routes } from '../constants/routes'
import { api, getApiErrorMessage } from '../services/api'

export function HomePage({ navigate }) {
  const services = [
    ['Visa guidance', 'Personalized migration routes and requirement mapping.'],
    ['Document readiness', 'Checklist and review pipeline for every application.'],
    ['AI-powered scoring', 'Readiness scoring to improve approval probability.'],
    ['Study placement support', 'Program matching by budget, intake, and country.'],
    ['Job relocation support', 'Skills profile plus visa sponsorship targeting.'],
    ['Consultant assistance', 'Collaborate with experts and get action notes.'],
    ['Secure payment access', 'Paystack-ready checkout and subscription controls.'],
  ]

  return (
    <section className="stack">
      <div className="hero card">
        <p className="eyebrow">Immigration-tech SaaS</p>
        <h1>VisaPilot helps you plan, score, and execute your global move.</h1>
        <p>
          One platform for visa guidance, document preparedness, AI insights, study placement, job
          relocation, consultant workflows, and secure payment access.
        </p>
        <div className="button-row">
          <button className="primary-btn" type="button" onClick={() => navigate(routes.login)}>
            Login
          </button>
          <button className="secondary-btn" type="button" onClick={() => navigate(routes.register)}>
            Register
          </button>
          <button className="ghost-btn" type="button" onClick={() => navigate(routes.pricing)}>
            Pricing
          </button>
        </div>
      </div>

      <div className="grid-3">
        {services.map(([title, description]) => (
          <ServiceCard key={title} title={title} description={description} />
        ))}
      </div>

      <div className="grid-4">
        {[
          ['Visa Assessment', routes.visaAssessment],
          ['Study Placement', routes.studyPlacement],
          ['Job Relocation', routes.jobRelocation],
          ['SOP Generator', routes.sopGenerator],
          ['Refusal Analysis', routes.refusalAnalysis],
        ].map(([label, path]) => (
          <button key={path} type="button" className="card action-card" onClick={() => navigate(path)}>
            {label}
          </button>
        ))}
      </div>
    </section>
  )
}

export function LoginPage({ navigate }) {
  const { login, loading, authError } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const submit = async (event) => {
    event.preventDefault()
    if (!email.trim() || !password) return
    const result = await login({ email: email.trim(), password })
    if (result.ok) navigate(routes.dashboard)
  }

  return (
    <form className="card form" onSubmit={submit}>
      <h2>Login</h2>
      <FormInput label="Email" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
      <FormInput
        label="Password"
        type="password"
        required
        minLength={8}
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <AlertMessage type="error" message={authError} />
      <button className="primary-btn" type="submit" disabled={loading}>
        Sign In
      </button>
      {loading ? <LoadingSpinner label="Authenticating..." /> : null}
    </form>
  )
}

export function RegisterPage({ navigate }) {
  const { register, loading, authError } = useAuth()
  const [form, setForm] = useState({ full_name: '', email: '', password: '', password_confirm: '' })
  const [localError, setLocalError] = useState('')

  const onChange = (key, value) => setForm((prev) => ({ ...prev, [key]: value }))
  const submit = async (event) => {
    event.preventDefault()
    setLocalError('')

    const missing = []
    if (!form.full_name.trim()) missing.push('Full name is required.')
    if (!form.email.trim()) missing.push('Email is required.')
    if (!form.password) missing.push('Password is required.')
    if (missing.length) {
      setLocalError(missing.join('\n'))
      return
    }

    if (form.password.length < 8) {
      setLocalError('Password must be at least 8 characters.')
      return
    }

    if (form.password_confirm && form.password !== form.password_confirm) {
      setLocalError('Passwords do not match.')
      return
    }
    
    const normalizedEmail = form.email.trim().toLowerCase()
    const payload = {
      full_name: form.full_name.trim(),
      name: form.full_name.trim(),
      email: normalizedEmail,
      username: normalizedEmail,
      password: form.password,
      password_confirm: form.password_confirm,
    }

    const result = await register(payload)
    if (result.ok) navigate(routes.dashboard)
  }

  return (
    <form className="card form" onSubmit={submit}>
      <h2>Register</h2>
      <FormInput label="Full Name" required value={form.full_name} onChange={(e) => onChange('full_name', e.target.value)} />
      <FormInput label="Email" type="email" required value={form.email} onChange={(e) => onChange('email', e.target.value)} />
      <FormInput label="Password" type="password" required minLength={8} value={form.password} onChange={(e) => onChange('password', e.target.value)} />
      <FormInput label="Confirm Password" type="password" value={form.password_confirm} onChange={(e) => onChange('password_confirm', e.target.value)} />
      <AlertMessage type="error" message={localError || authError} />
      <button className="primary-btn" type="submit" disabled={loading}>
        Create Account
      </button>
    </form>
  )
}

export function DashboardPage({ navigate }) {
  const { profile, accessToken } = useAuth()
  const [subscription, setSubscription] = useState(null)

  React.useEffect(() => {
    let ignore = false
    api.currentSubscription(accessToken).then((data) => !ignore && setSubscription(data)).catch(() => {})
    return () => {
      ignore = true
    }
  }, [accessToken])

  return (
    <section className="stack">
      <h2>Dashboard</h2>
      <div className="grid-4">
        <DashboardCard title="Profile" value={profile?.full_name || profile?.email || 'Applicant'} note="Account summary" />
        <DashboardCard title="Visa Readiness" value="72 / 100" note="AI scoring estimate" />
        <DashboardCard title="Document Status" value="8 / 12 ready" note="Pending reviews in queue" />
        <DashboardCard title="Active Applications" value="2" note="Study permit + work visa" />
      </div>
      <div className="card">
        <h3>Subscription Status</h3>
        <p>{subscription?.plan || 'No active plan found. Select a package to continue.'}</p>
      </div>
      <div className="button-row">
        {[['Start Assessment', routes.visaAssessment], ['Upload Documents', routes.documents], ['Go to Payment', routes.payment]].map(([label, path]) => (
          <button key={path} className="secondary-btn" type="button" onClick={() => navigate(path)}>
            {label}
          </button>
        ))}
      </div>
    </section>
  )
}

function GenericFormPage({ title, description, fields, onSubmitLabel = 'Submit', onSubmit }) {
  const initial = useMemo(() => Object.fromEntries(fields.map((f) => [f.name, ''])), [fields])
  const [form, setForm] = useState(initial)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    const missingFields = fields
      .filter((field) => field.required !== false && !String(form[field.name] || '').trim())
      .map((field) => `${field.label} is required.`)

    if (missingFields.length) {
      setError(missingFields.join('\n'))
      return
    }

    setLoading(true)
    setError('')
    setMessage('')
    try {
      await onSubmit(form)
      setMessage('Submitted successfully.')
    } catch (err) {
      setError(getApiErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <form className="card form" onSubmit={handleSubmit}>
      <h2>{title}</h2>
      <p>{description}</p>
      {fields.map((field) => (
        <FormInput
          key={field.name}
          label={field.label}
          as={field.type === 'textarea' ? 'textarea' : 'input'}
          type={field.type === 'textarea' ? undefined : field.type || 'text'}
          value={form[field.name]}
          onChange={(e) => setForm((prev) => ({ ...prev, [field.name]: e.target.value }))}
          required={field.required !== false}
        />
      ))}
      <AlertMessage type="success" message={message} />
      <AlertMessage type="error" message={error} />
      <button className="primary-btn" type="submit" disabled={loading}>
        {onSubmitLabel}
      </button>
    </form>
  )
}

export function VisaAssessmentPage() {
  const { accessToken } = useAuth()
  return (
    <GenericFormPage
      title="Visa Assessment"
      description="Guided AI scoring form for eligibility and readiness."
      fields={[
        { name: 'destination_country', label: 'Destination country' },
        { name: 'visa_category', label: 'Visa category' },
        { name: 'age', label: 'Age', type: 'number' },
        { name: 'education_level', label: 'Education level' },
        { name: 'work_experience', label: 'Work experience' },
        { name: 'travel_history', label: 'Travel history', type: 'textarea' },
        { name: 'financial_proof', label: 'Financial proof' },
        { name: 'family_ties', label: 'Family ties' },
        { name: 'purpose_of_travel', label: 'Purpose of travel', type: 'textarea' },
      ]}
      onSubmit={(data) =>
        api.submitVisaAssessment(accessToken, {
          age: Number(data.age),
          country: data.destination_country,
          education_level: data.education_level,
          work_experience: data.work_experience,
        })
      }
    />
  )
}

export function DocumentChecklistPage() {
  const rows = ['Passport', 'Bank statement', 'Admission letter', 'Employment letter', 'SOP', 'Invitation letter']
  return (
    <section className="card">
      <h2>Document Checklist</h2>
      <p>Track required documents by visa type with review statuses.</p>
      <ul className="status-list">
        {rows.map((row) => (
          <li key={row}>
            <strong>{row}</strong> <span>missing / uploaded / under review / approved / rejected</span>
          </li>
        ))}
      </ul>
    </section>
  )
}

export function DocumentsPage() {
  return (
    <section className="card">
      <h2>Documents Upload</h2>
      <p>Upload passport, bank statement, admission letter, employment letter, SOP, invitation letter, and supporting files.</p>
      <div className="grid-3">
        {['Passport', 'Bank statement', 'Admission letter', 'Employment letter', 'SOP', 'Invitation letter', 'Supporting documents'].map((item) => (
          <label key={item} className="form-input card">
            <span>{item}</span>
            <input type="file" />
          </label>
        ))}
      </div>
    </section>
  )
}

export function SopGeneratorPage() {
  const { accessToken } = useAuth()
  return (
    <GenericFormPage
      title="SOP Generator"
      description="Generate an AI-ready SOP draft from your profile context."
      fields={[
        { name: 'background', label: 'Applicant background', type: 'textarea' },
        { name: 'education', label: 'Education' },
        { name: 'work_history', label: 'Work history', type: 'textarea' },
        { name: 'goal', label: 'Study/work goal' },
        { name: 'country_choice', label: 'Country choice' },
        { name: 'financial_sponsor', label: 'Financial sponsor' },
        { name: 'home_ties', label: 'Home ties', type: 'textarea' },
        { name: 'career_plan', label: 'Career plan', type: 'textarea' },
      ]}
      onSubmit={(data) => api.generateSOP(accessToken, data)}
    />
  )
}

export function RefusalAnalysisPage() {
  const { accessToken } = useAuth()
  return (
    <GenericFormPage
      title="Refusal Analysis"
      description="Paste refusal letter text or upload document to identify corrections and reapplication strategy."
      fields={[{ name: 'refusal_text', label: 'Refusal letter text', type: 'textarea' }]}
      onSubmit={(data) => api.analyzeRefusal(accessToken, data)}
    />
  )
}

export function StudyPlacementPage() {
  return (
    <GenericFormPage
      title="Study Placement"
      description="Program matching by country, budget, and academic goals."
      fields={[
        { name: 'country', label: 'Country' },
        { name: 'education_level', label: 'Education level' },
        { name: 'budget', label: 'Budget' },
        { name: 'field_of_study', label: 'Field of study' },
        { name: 'preferred_intake', label: 'Preferred intake' },
        { name: 'english_test_status', label: 'English test status' },
      ]}
      onSubmit={async () => Promise.resolve()}
    />
  )
}

export function JobRelocationPage() {
  return (
    <GenericFormPage
      title="Job Relocation"
      description="Build relocation profile for sponsored opportunities."
      fields={[
        { name: 'skills', label: 'Skills', type: 'textarea' },
        { name: 'years_of_experience', label: 'Years of experience', type: 'number' },
        { name: 'occupation', label: 'Occupation' },
        { name: 'preferred_country', label: 'Preferred country' },
        { name: 'visa_sponsorship_preference', label: 'Visa sponsorship preference' },
      ]}
      onSubmit={async () => Promise.resolve()}
    />
  )
}

const plans = [
  { name: 'Starter', price: '$19/mo', features: ['Checklist', 'Basic scoring', 'Single applicant'] },
  { name: 'Pro', price: '$49/mo', features: ['AI scoring', 'SOP + refusal analysis', 'Priority support'] },
  { name: 'Premium', price: '$99/mo', features: ['Consultant access', 'Advanced analytics', 'Team features'] },
]

export function PricingPage({ navigate }) {
  return (
    <section className="stack">
      <h2>Pricing</h2>
      <div className="grid-3">
        {plans.map((plan) => (
          <PlanCard key={plan.name} plan={plan} onSelect={() => navigate(`${routes.payment}?plan=${encodeURIComponent(plan.name)}`)} />
        ))}
      </div>
    </section>
  )
}

export function PaymentPage({ navigate }) {
  const { accessToken } = useAuth()
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const search = new URLSearchParams(window.location.search)
  const selectedPlan = search.get('plan') || 'Starter'

  const startPayment = async () => {
    setLoading(true)
    setError('')
    try {
      const result = await api.initializePayment(accessToken, { plan: selectedPlan, provider: 'paystack' })
      if (result?.authorization_url) {
        window.location.href = result.authorization_url
        return
      }
      navigate(routes.paymentSuccess)
    } catch (err) {
      setError(getApiErrorMessage(err, 'Payment initialization failed'))
      navigate(routes.paymentFailed)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="card">
      <h2>Checkout</h2>
      <p>Selected plan: {selectedPlan}</p>
      <p>Paystack is configured as the primary payment provider.</p>
      <button className="primary-btn" type="button" onClick={startPayment} disabled={loading}>
        Initialize payment
      </button>
      <AlertMessage type="error" message={error} />
    </section>
  )
}

export function PaymentSuccessPage() {
  return <section className="card"><h2>Payment Successful</h2><p>Your subscription is now active.</p></section>
}

export function PaymentFailedPage() {
  return <section className="card"><h2>Payment Failed</h2><p>We could not verify the transaction. Please retry from checkout.</p></section>
}

export function ProfilePage() {
  const { profile } = useAuth()
  return (
    <section className="card">
      <h2>Profile</h2>
      <p>Name: {profile?.full_name || 'Not provided'}</p>
      <p>Email: {profile?.email || 'Not provided'}</p>
    </section>
  )
}

export function ConsultantDashboardPage() {
  return (
    <section className="card">
      <h2>Consultant Dashboard</h2>
      <p>Users, applications, document reviews, payments, consultant notes, and analytics summary.</p>
    </section>
  )
}

const adminRoles = [
  'SUPER_ADMIN',
  'PLATFORM_ADMIN',
  'APPLICANT',
  'IMMIGRATION_CONSULTANT',
  'RECRUITER',
  'EMPLOYER',
  'SCHOOL_ADMIN',
  'AGENT',
  'SUPPORT_STAFF',
]

export function AdminDashboardPage() {

  const { accessToken } = useAuth()
  const [overview, setOverview] = useState(null)
  const [users, setUsers] = useState([])
  const [search, setSearch] = useState('')
  const [selectedRole, setSelectedRole] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState({ full_name: '', email: '', role: 'APPLICANT', password: '' })

  const loadDashboard = React.useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const [overviewData, usersData] = await Promise.all([
        api.adminOverview(accessToken),
        api.adminListUsers(accessToken, {
          ...(search.trim() ? { q: search.trim() } : {}),
          ...(selectedRole ? { role: selectedRole } : {}),
        }),
      ])
      setOverview(overviewData)
      setUsers(usersData.results || [])
    } catch (err) {
      setError(getApiErrorMessage(err, 'Unable to load admin dashboard.'))
    } finally {
      setLoading(false)
    }
  }, [accessToken, search, selectedRole])

  React.useEffect(() => {
    loadDashboard()
  }, [loadDashboard])

  const onCreateUser = async (event) => {
    event.preventDefault()
    setSaving(true)
    setError('')
    setSuccess('')
    try {
      await api.adminCreateUser(accessToken, {
        full_name: form.full_name.trim(),
        email: form.email.trim(),
        role: form.role,
        password: form.password,
      })
      setSuccess('User created successfully.')
      setForm({ full_name: '', email: '', role: 'APPLICANT', password: '' })
      loadDashboard()
    } catch (err) {
      setError(getApiErrorMessage(err, 'Unable to create user.'))
    } finally {
      setSaving(false)
    }
  }

  return (
    <section className="stack">
      <h2>Admin Dashboard</h2>
      <p>Manage platform users, roles, and operational visibility from one place.</p>
      {loading ? <LoadingSpinner label="Loading admin dashboard..." /> : null}
      <AlertMessage type="error" message={error} />
      <AlertMessage type="success" message={success} />

      <div className="grid-3">
        <DashboardCard title="Total Users" value={overview?.total_users ?? 0} note="All registered accounts" />
        <DashboardCard title="Active Users" value={overview?.active_users ?? 0} note="Accounts currently enabled" />
        <DashboardCard title="Inactive Users" value={overview?.inactive_users ?? 0} note="Accounts currently disabled" />
      </div>

      <div className="grid-3">
        <section className="card">
          <h3>Create User</h3>
          <form className="form" onSubmit={onCreateUser}>
            <FormInput label="Full Name" required value={form.full_name} onChange={(e) => setForm((prev) => ({ ...prev, full_name: e.target.value }))} />
            <FormInput label="Email" type="email" required value={form.email} onChange={(e) => setForm((prev) => ({ ...prev, email: e.target.value }))} />
            <FormInput label="Role" as="select" value={form.role} onChange={(e) => setForm((prev) => ({ ...prev, role: e.target.value }))}>
              {adminRoles.map((role) => (
                <option key={role} value={role}>{role}</option>
              ))}
            </FormInput>
            <FormInput label="Temporary Password" type="password" required minLength={8} value={form.password} onChange={(e) => setForm((prev) => ({ ...prev, password: e.target.value }))} />
            <button className="primary-btn" type="submit" disabled={saving}>{saving ? 'Creating...' : 'Create User'}</button>
          </form>
        </section>

        <section className="card">
          <h3>Role Breakdown</h3>
          <ul className="status-list">
            {(overview?.role_breakdown || []).map((item) => (
              <li key={item.role}><strong>{item.role}</strong> <span>{item.total}</span></li>
            ))}
          </ul>
        </section>

        <section className="card">
          <h3>Recent Users</h3>
          <ul className="status-list">
            {(overview?.recent_users || []).map((user) => (
              <li key={user.id}><strong>{user.full_name || user.email}</strong> <span>{user.role}</span></li>
            ))}
          </ul>
        </section>
      </div>

      <section className="card">
        <div className="button-row">
          <FormInput label="Search" value={search} onChange={(e) => setSearch(e.target.value)} />
          <FormInput label="Filter role" as="select" value={selectedRole} onChange={(e) => setSelectedRole(e.target.value)}>
            <option value="">All roles</option>
            {adminRoles.map((role) => (
              <option key={role} value={role}>{role}</option>
            ))}
          </FormInput>
          <button className="secondary-btn" type="button" onClick={loadDashboard}>Refresh</button>
        </div>
        <h3>Users</h3>
        <div className="table-wrap">
          <table className="admin-table">
            <thead>
              <tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th></tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.full_name || '—'}</td>
                  <td>{user.email}</td>
                  <td>{user.role}</td>
                  <td>{user.is_active ? 'Active' : 'Inactive'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  )
}

export function NotFoundPage() {
  return <section className="card"><h2>Page not found</h2></section>
}
