DASHBOARD_TEMPLATE = """export default function Dashboard() {
  const [activeTab, setActiveTab] = React.useState('Overview');

  // Sidebar Items
  const sidebarItems = [
    { label: 'Overview', icon: 'LayoutDashboard', onClick: () => setActiveTab('Overview') },
    { label: 'Analytics', icon: 'BarChart2', onClick: () => setActiveTab('Analytics') },
    { label: 'Settings', icon: 'Settings', onClick: () => setActiveTab('Settings') }
  ];

  // Navbar Links
  const navbarLinks = [
    { label: 'Help', href: '#' },
    { label: 'Profile', href: '#' }
  ];
  
  // User Profile
  const user = {
    name: "Alex Designer",
    avatar: "https://i.pravatar.cc/150?u=a042581f4e29026704d"
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-black text-foreground font-sans antialiased overflow-hidden">
      {/* Sidebar Navigation - Glassmorphism */}
      <Sidebar 
        items={sidebarItems} 
        activeItem={activeTab} 
        position="left" 
        className="hidden md:flex glass border-none z-10"
      />
      
      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden relative">
        <Navbar brand="{{BRAND_NAME}}" links={navbarLinks} user={user} className="sticky top-0 z-10 backdrop-blur-md bg-transparent border-b border-white/10" />
        
        {/* Decorative background blobs */}
        <div className="absolute top-0 left-0 w-96 h-96 bg-{{PRIMARY_COLOR}}-500/20 rounded-full blur-3xl -z-10 translate-x-1/2 translate-y-1/2 pointer-events-none"></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl -z-10 -translate-x-1/2 -translate-y-1/2 pointer-events-none"></div>

        <main className="flex-1 overflow-y-auto p-6 scroll-smooth">
          <div className="max-w-7xl mx-auto space-y-6">
             {/* Header Section */}
             <div className="flex justify-between items-center mb-6">
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                   <h1 className="text-4xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-400">
                     Dashboard Overview
                   </h1>
                   <p className="text-muted-foreground mt-2">Welcome back, {user.name}</p>
                </div>
                <div className="flex gap-3">
                   <Button variant="outline" size="sm" className="glass-card hover:bg-white/40">Export Report</Button>
                   <Button variant="primary" size="sm" className="shadow-lg shadow-{{PRIMARY_COLOR}}-500/20" onClick={() => alert('Add New Clicked')}>+ Add New</Button>
                </div>
             </div>
             
             {/* Key Metrics Cards */}
             <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                <Card className="glass-card border-none hover:-translate-y-1 transition-transform duration-300">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-3 bg-{{PRIMARY_COLOR}}-500/10 rounded-2xl">
                            <Lucide.Users className="w-6 h-6 text-{{PRIMARY_COLOR}}-600 dark:text-{{PRIMARY_COLOR}}-400" />
                        </div>
                        <span className="text-xs font-bold text-emerald-600 bg-emerald-100 dark:text-emerald-400 dark:bg-emerald-900/30 px-2 py-1 rounded-full border border-emerald-200 dark:border-emerald-800">+12.5%</span>
                    </div>
                    <div>
                        <p className="text-sm font-medium text-muted-foreground">Total Users</p>
                        <h3 className="text-3xl font-bold mt-1 tracking-tight">12,345</h3>
                    </div>
                </Card>
                
                 <Card className="glass-card border-none hover:-translate-y-1 transition-transform duration-300">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-3 bg-{{PRIMARY_COLOR}}-500/10 rounded-2xl">
                            <Lucide.DollarSign className="w-6 h-6 text-{{PRIMARY_COLOR}}-600 dark:text-{{PRIMARY_COLOR}}-400" />
                        </div>
                        <span className="text-xs font-bold text-emerald-600 bg-emerald-100 dark:text-emerald-400 dark:bg-emerald-900/30 px-2 py-1 rounded-full border border-emerald-200 dark:border-emerald-800">+8.2%</span>
                    </div>
                    <div>
                        <p className="text-sm font-medium text-muted-foreground">Total Revenue</p>
                        <h3 className="text-3xl font-bold mt-1 tracking-tight">$45,200</h3>
                    </div>
                </Card>
                
                 <Card className="glass-card border-none hover:-translate-y-1 transition-transform duration-300">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-3 bg-{{PRIMARY_COLOR}}-500/10 rounded-2xl">
                            <Lucide.Activity className="w-6 h-6 text-{{PRIMARY_COLOR}}-600 dark:text-{{PRIMARY_COLOR}}-400" />
                        </div>
                        <span className="text-xs font-bold text-gray-500 bg-gray-100 px-2 py-1 rounded-full">Active</span>
                    </div>
                    <div>
                        <p className="text-sm font-medium text-muted-foreground">Active Sessions</p>
                        <h3 className="text-3xl font-bold mt-1 tracking-tight">894</h3>
                    </div>
                </Card>
             </div>
             
             {/* Charts & Tables Section */}
             <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
               <Card className="lg:col-span-2 glass-card border-none" title="Revenue Growth">
                  <div className="mt-4">
                    <Chart type="bar" color="{{PRIMARY_COLOR}}" />
                  </div>
               </Card>
               
               <Card title="Traffic Sources" className="glass-card border-none">
                  <div className="mt-4">
                    <Chart type="pie" color="{{PRIMARY_COLOR}}" />
                  </div>
               </Card>
             </div>
             
             <Card title="Recent Transactions" className="glass-card border-none overflow-hidden">
               <Table 
                 headers={["User", "Date", "Amount", "Status"]}
                 data={[
                   { user: "John Doe", date: "Oct 24, 2024", amount: "$120.00", status: "Completed" },
                   { user: "Jane Smith", date: "Oct 23, 2024", amount: "$250.00", status: "Pending" },
                   { user: "Bob Johnson", date: "Oct 22, 2024", amount: "$99.00", status: "Completed" },
                   { user: "Alice Brown", date: "Oct 21, 2024", amount: "$450.00", status: "Failed" },
                 ]}
                 className="mt-4"
               />
            </Card>
          </div>
        </main>
      </div>
    </div>
  );
}"""

LOGIN_TEMPLATE = """export default function LoginPage() {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [isLoading, setIsLoading] = React.useState(false);

  // Handle Login Logic
  const handleLogin = () => {
    setIsLoading(true);
    // Simulate API call
    setTimeout(() => {
        setIsLoading(false);
        alert('Login Successful (Simulation)');
    }, 2000);
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100 dark:bg-black p-4 relative overflow-hidden">
      
      {/* Dynamic Background */}
      <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 brightness-100 contrast-150 mix-blend-overlay"></div>
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-{{PRIMARY_COLOR}}-500/30 rounded-full blur-[120px] -translate-y-1/2 translate-x-1/2"></div>
      <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-purple-500/30 rounded-full blur-[120px] translate-y-1/2 -translate-x-1/2"></div>

      {/* Authentication Card */}
      <Card className="glass w-full max-w-md p-8 rounded-3xl border-white/20 dark:border-white/10 relative z-10 backdrop-blur-xl">
        
        <div className="text-center mb-8">
          <div className="inline-flex justify-center items-center w-16 h-16 rounded-2xl bg-gradient-to-tr from-{{PRIMARY_COLOR}}-500 to-purple-600 shadow-lg shadow-{{PRIMARY_COLOR}}-500/30 mb-6 group">
             <Lucide.Lock className="w-8 h-8 text-white group-hover:scale-110 transition-transform duration-300" />
          </div>
          <h1 className="text-3xl font-extrabold text-foreground mb-2 tracking-tight">Welcome Back</h1>
          <p className="text-muted-foreground">Enter your credentials to access your account</p>
        </div>
        
        <div className="space-y-6">
          <div className="space-y-2">
            <Input 
                label="Email Address" 
                type="email" 
                placeholder="name@company.com" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                icon={Lucide.Mail}
                className="bg-white/50 dark:bg-black/50 border-transparent focus:border-{{PRIMARY_COLOR}}-500 h-12"
            />
          </div>
          
          <div className="space-y-2">
              <Input 
                label="Password" 
                type="password" 
                placeholder="••••••••" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                icon={Lucide.Lock}
                className="bg-white/50 dark:bg-black/50 border-transparent focus:border-{{PRIMARY_COLOR}}-500 h-12"
              />
              <div className="flex justify-end">
                  <a href="#" className="text-xs font-medium text-{{PRIMARY_COLOR}}-600 hover:text-{{PRIMARY_COLOR}}-500 dark:text-{{PRIMARY_COLOR}}-400">Forgot password?</a>
              </div>
          </div>
          
          <Button 
            className="w-full h-12 text-base font-semibold bg-gradient-to-r from-{{PRIMARY_COLOR}}-600 to-purple-600 hover:from-{{PRIMARY_COLOR}}-500 hover:to-purple-500 text-white shadow-lg shadow-{{PRIMARY_COLOR}}-500/30 transition-all transform hover:-translate-y-0.5" 
            variant="primary" 
            size="lg"
            onClick={handleLogin}
            loading={isLoading}
          >
            Sign In
          </Button>
          
          <div className="relative my-8">
            <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-gray-200 dark:border-gray-800"></div></div>
            <div className="relative flex justify-center text-xs uppercase"><span className="px-3 bg-white/0 text-muted-foreground backdrop-blur-sm">Or continue with</span></div>
          </div>
          
           <div className="grid grid-cols-2 gap-4">
             <Button variant="outline" className="w-full flex items-center justify-center gap-2 h-10 bg-white/50 hover:bg-white/80 dark:bg-black/50 dark:hover:bg-black/80">
               <Lucide.Github className="w-4 h-4" /> Github
             </Button>
             <Button variant="outline" className="w-full flex items-center justify-center gap-2 h-10 bg-white/50 hover:bg-white/80 dark:bg-black/50 dark:hover:bg-black/80">
               <Lucide.Twitter className="w-4 h-4 text-blue-400" /> Twitter
             </Button>
          </div>
        </div>
        
        <div className="mt-8 text-center text-sm">
          <span className="text-muted-foreground">Don't have an account? </span>
          <a href="#" className="font-bold text-{{PRIMARY_COLOR}}-600 hover:text-{{PRIMARY_COLOR}}-500 dark:text-{{PRIMARY_COLOR}}-400 hover:underline transition-colors">Create free account</a>
        </div>
      </Card>
    </div>
  );
}"""

CONTACT_TEMPLATE = """export default function ContactForm() {
  const [formData, setFormData] = React.useState({
    firstName: '',
    lastName: '',
    email: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = React.useState(false);

  const handleSubmit = () => {
    setIsSubmitting(true);
    setTimeout(() => {
        setIsSubmitting(false);
        alert('Message Sent!');
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex items-center justify-center p-4 sm:p-6 lg:p-8 relative overflow-hidden">
       {/* Background Decoration */}
       <div className="absolute -top-40 -right-40 w-[600px] h-[600px] bg-{{PRIMARY_COLOR}}-500/20 rounded-full blur-[100px] pointer-events-none"></div>
       <div className="absolute -bottom-40 -left-40 w-[600px] h-[600px] bg-indigo-500/20 rounded-full blur-[100px] pointer-events-none"></div>

      <div className="max-w-5xl w-full grid grid-cols-1 lg:grid-cols-2 gap-0 bg-white dark:bg-gray-900 rounded-3xl shadow-2xl overflow-hidden glass border border-white/20 dark:border-white/10">
        
        {/* Info Section */}
        <div className="bg-gradient-to-br from-{{PRIMARY_COLOR}}-600 to-indigo-700 p-10 text-white flex flex-col justify-between relative overflow-hidden">
           {/* Abstract Shapes */}
           <div className="absolute top-10 right-10 w-20 h-20 bg-white/10 rounded-full blur-xl"></div>
           <div className="absolute bottom-10 left-10 w-32 h-32 bg-black/10 rounded-full blur-xl"></div>
           
           <div className="relative z-10">
               <h2 className="text-4xl font-extrabold mb-6 tracking-tight">Get in touch</h2>
               <p className="text-{{PRIMARY_COLOR}}-100 mb-10 text-lg leading-relaxed">
                 Fill in the form to start a conversation with our team. We typically respond within 24 hours.
               </p>
               
               <div className="space-y-8">
                 <div className="flex items-center gap-5">
                    <div className="p-3 bg-white/10 rounded-lg backdrop-blur-sm">
                        <Lucide.MapPin className="w-6 h-6 text-{{PRIMARY_COLOR}}-100" />
                    </div>
                    <span className="text-lg">123 Innovation Drive, Tech Valley, CA</span>
                 </div>
                 <div className="flex items-center gap-5">
                    <div className="p-3 bg-white/10 rounded-lg backdrop-blur-sm">
                        <Lucide.Phone className="w-6 h-6 text-{{PRIMARY_COLOR}}-100" />
                    </div>
                    <span className="text-lg">+1 (555) 000-0000</span>
                 </div>
                 <div className="flex items-center gap-5">
                    <div className="p-3 bg-white/10 rounded-lg backdrop-blur-sm">
                        <Lucide.Mail className="w-6 h-6 text-{{PRIMARY_COLOR}}-100" />
                    </div>
                    <span className="text-lg">contact@ryze.ai</span>
                 </div>
               </div>
           </div>
           
           <div className="flex gap-4 mt-12 relative z-10">
              <Button size="icon" variant="ghost" className="text-white hover:bg-white/20 rounded-full w-12 h-12"><Lucide.Twitter className="w-5 h-5"/></Button>
              <Button size="icon" variant="ghost" className="text-white hover:bg-white/20 rounded-full w-12 h-12"><Lucide.Linkedin className="w-5 h-5"/></Button>
              <Button size="icon" variant="ghost" className="text-white hover:bg-white/20 rounded-full w-12 h-12"><Lucide.Instagram className="w-5 h-5"/></Button>
           </div>
        </div>

        {/* Form Section */}
        <div className="p-10 lg:p-14 bg-white/50 dark:bg-black/50 backdrop-blur-md">
            <h3 className="text-2xl font-bold text-foreground mb-8">Send us a Message</h3>
            <div className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                 <Input label="First Name" placeholder="John" className="bg-transparent" />
                 <Input label="Last Name" placeholder="Doe" className="bg-transparent" />
              </div>
              <Input label="Email Address" type="email" placeholder="john@example.com" className="bg-transparent" />
              <div className="flex flex-col gap-2 w-full">
                  <label className="text-sm font-medium text-muted-foreground ml-1">Message</label>
                  <textarea 
                    className="flex min-h-[150px] w-full rounded-xl border border-input bg-transparent px-4 py-3 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 resize-none transition-shadow"
                    placeholder="Tell us about your project..."
                  />
              </div>
              
              <div className="flex justify-end pt-6">
                <Button 
                   className="w-full sm:w-auto h-12 px-8 text-base bg-foreground text-background hover:bg-foreground/90 transition-all shadow-lg" 
                   onClick={handleSubmit}
                   loading={isSubmitting}
                >
                  Send Message
                </Button>
              </div>
            </div>
        </div>
      </div>
    </div>
  );
}"""


LANDING_TEMPLATE = """export default function LandingPage() {
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);

  // Smooth scroll
  const scrollTo = (id) => {
    const element = document.getElementById(id);
    if (element) element.scrollIntoView({ behavior: 'smooth' });
    setIsMenuOpen(false);
  };

  return (
    <div className="flex flex-col min-h-screen bg-background font-sans text-foreground selection:bg-{{PRIMARY_COLOR}}-500/30">
      
      {/* Navigation */}
      <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/80 backdrop-blur-md">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-2">
            <div className="bg-gradient-to-tr from-{{PRIMARY_COLOR}}-600 to-purple-600 p-2 rounded-xl">
               <Lucide.Sparkles className="h-5 w-5 text-white" />
            </div>
            <span className="font-bold text-xl tracking-tight">{{BRAND_NAME}}</span>
          </div>
          
          <div className="hidden md:flex gap-8 items-center">
            {['Features', 'Testimonials', 'Pricing'].map((item) => (
               <button key={item} onClick={() => scrollTo(item.toLowerCase())} className="text-sm font-medium text-muted-foreground hover:text-{{PRIMARY_COLOR}}-600 transition-colors">
                  {item}
               </button>
            ))}
            <Button variant="primary" className="bg-{{PRIMARY_COLOR}}-600 hover:bg-{{PRIMARY_COLOR}}-700 text-white shadow-lg shadow-{{PRIMARY_COLOR}}-500/25">
               Get Started
            </Button>
          </div>

          <button className="md:hidden" onClick={() => setIsMenuOpen(!isMenuOpen)}>
             {isMenuOpen ? <Lucide.X className="h-6 w-6" /> : <Lucide.Menu className="h-6 w-6" />}
          </button>
        </div>
        
        {/* Mobile Menu */}
        {isMenuOpen && (
           <div className="md:hidden p-4 border-t bg-background space-y-4 animate-in slide-in-from-top-2">
              {['Features', 'Testimonials', 'Pricing'].map((item) => (
                 <button key={item} onClick={() => scrollTo(item.toLowerCase())} className="block w-full text-left py-2 font-medium">
                    {item}
                 </button>
              ))}
               <Button className="w-full bg-{{PRIMARY_COLOR}}-600 text-white">Get Started</Button>
           </div>
        )}
      </header>
      
      <main className="flex-1">
      
        {/* Hero Section */}
        <section className="relative pt-24 pb-32 overflow-hidden">
           <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-{{PRIMARY_COLOR}}-500/20 rounded-full blur-[120px] -z-10 pointer-events-none"></div>
           
           <div className="container mx-auto px-4 text-center">
              <div className="inline-flex items-center rounded-full border border-{{PRIMARY_COLOR}}-200 bg-{{PRIMARY_COLOR}}-50 dark:border-{{PRIMARY_COLOR}}-800 dark:bg-{{PRIMARY_COLOR}}-900/20 px-3 py-1 text-sm font-medium text-{{PRIMARY_COLOR}}-600 dark:text-{{PRIMARY_COLOR}}-400 mb-6 backdrop-blur-sm">
                 <span className="flex h-2 w-2 rounded-full bg-{{PRIMARY_COLOR}}-600 mr-2 animate-pulse"></span>
                 New Version 2.0 Released
              </div>
              
              <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-b from-foreground to-foreground/60 mb-6">
                 Build faster with <br className="hidden md:block"/>
                 <span className="bg-clip-text text-transparent bg-gradient-to-r from-{{PRIMARY_COLOR}}-600 to-purple-600">{{BRAND_NAME}}</span>
              </h1>
              
              <p className="mx-auto max-w-[700px] text-lg text-muted-foreground mb-10 leading-relaxed">
                 The ultimate platform for modern developers. Deterministic, scalable, and built for performance. Start building your dream project today.
              </p>
              
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                 <Button size="lg" className="h-12 px-8 text-base bg-{{PRIMARY_COLOR}}-600 hover:bg-{{PRIMARY_COLOR}}-700 text-white shadow-xl shadow-{{PRIMARY_COLOR}}-500/20 hover:scale-105 transition-transform">
                    Start Building Free
                 </Button>
                 <Button size="lg" variant="outline" className="h-12 px-8 text-base hover:bg-muted/50 backdrop-blur-sm">
                    <Lucide.Play className="mr-2 h-4 w-4" /> Watch Demo
                 </Button>
              </div>
              
              {/* Hero Image / Dashboard Preview */}
              <div className="mt-20 relative mx-auto max-w-5xl">
                 <div className="rounded-xl border bg-background/50 backdrop-blur shadow-2xl overflow-hidden p-2 ring-1 ring-inset ring-foreground/10">
                    <div className="rounded-lg bg-foreground/5 aspect-[16/9] flex items-center justify-center relative overflow-hidden group">
                       <div className="absolute inset-0 bg-gradient-to-tr from-{{PRIMARY_COLOR}}-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
                       {/* Mock UI Elements */}
                       <div className="w-[80%] h-[80%] bg-white dark:bg-black rounded-lg shadow-xl border border-border flex">
                          <div className="w-1/4 h-full border-r border-border p-4 space-y-2 hidden md:block">
                             <div className="h-2 w-1/2 bg-muted rounded mb-6"></div>
                             {[1,2,3,4].map(i => <div key={i} className="h-8 w-full bg-muted/50 rounded"></div>)}
                          </div>
                          <div className="flex-1 p-6 space-y-4">
                             <div className="h-8 w-1/3 bg-muted rounded mb-8"></div>
                             <div className="grid grid-cols-2 gap-4">
                                <div className="h-32 bg-{{PRIMARY_COLOR}}-50/50 dark:bg-{{PRIMARY_COLOR}}-900/10 border border-{{PRIMARY_COLOR}}-100 dark:border-{{PRIMARY_COLOR}}-800 rounded"></div>
                                <div className="h-32 bg-purple-50/50 dark:bg-purple-900/10 border border-purple-100 dark:border-purple-800 rounded"></div>
                             </div>
                             <div className="h-40 bg-muted/30 rounded border border-border"></div>
                          </div>
                       </div>
                    </div>
                 </div>
                 <div className="absolute -z-10 -bottom-10 -right-10 w-64 h-64 bg-purple-500/30 rounded-full blur-[80px] pointer-events-none"></div>
                 <div className="absolute -z-10 -top-10 -left-10 w-64 h-64 bg-{{PRIMARY_COLOR}}-500/30 rounded-full blur-[80px] pointer-events-none"></div>
              </div>
           </div>
        </section>
        
        {/* Features Grid */}
        <section id="features" className="py-24 bg-muted/30 relative">
           <div className="container mx-auto px-4">
              <div className="text-center max-w-3xl mx-auto mb-16">
                 <h2 className="text-3xl font-bold tracking-tight mb-4">Everything you need to scale</h2>
                 <p className="text-muted-foreground text-lg">Powerful features configured for production. Security, performance, and reliability out of the box.</p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                 {[
                    { title: "Deterministic AI", icon: Lucide.Brain, desc: "Zero hallucinations. Guaranteed valid code generation every time." },
                    { title: "Glassmorphism UI", icon: Lucide.Layers, desc: "Premium styling with blur effects and dynamic gradients built-in." },
                    { title: "Secure by Default", icon: Lucide.ShieldCheck, desc: "Enterprise-grade security standards with automated compliance." },
                    { title: "Microservices", icon: Lucide.Server, desc: "Independently scalable architecture for frontend, gateway, and engine." },
                    { title: "Real-time Sync", icon: Lucide.RefreshCw, desc: "Instant state synchronization across all connected clients." },
                    { title: "Global CDN", icon: Lucide.Globe, desc: "Deployed on edge networks for sub-millisecond latency worldwide." }
                 ].map((feature, i) => (
                    <div key={i} className="group relative overflow-hidden rounded-2xl border bg-background p-8 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                       <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                          <feature.icon className="w-24 h-24 text-{{PRIMARY_COLOR}}-500" />
                       </div>
                       <div className="mb-4 inline-flex items-center justify-center rounded-xl bg-{{PRIMARY_COLOR}}-50 dark:bg-{{PRIMARY_COLOR}}-900/20 p-3 text-{{PRIMARY_COLOR}}-600">
                          <feature.icon className="h-6 w-6" />
                       </div>
                       <h3 className="mb-2 text-xl font-bold">{feature.title}</h3>
                       <p className="text-muted-foreground">{feature.desc}</p>
                    </div>
                 ))}
              </div>
           </div>
        </section>
        
        {/* How It Works Section */}
        <section className="py-24 bg-background relative overflow-hidden">
           <div className="container mx-auto px-4">
              <div className="text-center max-w-3xl mx-auto mb-16">
                 <h2 className="text-3xl font-bold tracking-tight mb-4">How it works</h2>
                 <p className="text-muted-foreground text-lg">Three simple steps to launch your next big idea.</p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-12 relative">
                 {/* Connecting Line */}
                 <div className="hidden md:block absolute top-12 left-[16%] right-[16%] h-0.5 bg-gradient-to-r from-transparent via-{{PRIMARY_COLOR}}-200 dark:via-{{PRIMARY_COLOR}}-800 to-transparent -z-10"></div>
                 
                 {[
                    { step: "01", title: "Connect", desc: "Integrate with your existing data sources in minutes." },
                    { step: "02", title: "Configure", desc: "Customize the logic and UI to match your brand requirements." },
                    { step: "03", title: "Deploy", desc: "Launch globally with a single click to our edge network." }
                 ].map((item, i) => (
                    <div key={i} className="flex flex-col items-center text-center group">
                       <div className="w-24 h-24 rounded-full bg-white dark:bg-gray-900 border-4 border-{{PRIMARY_COLOR}}-50 dark:border-{{PRIMARY_COLOR}}-900/30 flex items-center justify-center text-2xl font-bold text-{{PRIMARY_COLOR}}-600 shadow-xl mb-6 group-hover:scale-110 transition-transform duration-300 relative z-10">
                          {item.step}
                       </div>
                       <h3 className="text-xl font-bold mb-3">{item.title}</h3>
                       <p className="text-muted-foreground leading-relaxed max-w-xs">{item.desc}</p>
                    </div>
                 ))}
              </div>
           </div>
        </section>

        {/* Pricing CTA */}
        <section id="pricing" className="py-24 relative overflow-hidden">
           <div className="container mx-auto px-4">
               <div className="rounded-3xl bg-gradient-to-r from-{{PRIMARY_COLOR}}-600 to-purple-600 p-12 text-center text-white relative overflow-hidden shadow-2xl">
                   <div className="absolute top-0 left-0 w-full h-full bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-overlay"></div>
                   <div className="relative z-10 max-w-2xl mx-auto">
                       <h2 className="text-3xl md:text-4xl font-bold mb-6">Ready to transform your workflow?</h2>
                       <p className="text-{{PRIMARY_COLOR}}-100 text-lg mb-8">Join thousands of developers building the future with {{BRAND_NAME}} today.</p>
                       <div className="flex flex-col sm:flex-row gap-4 justify-center">
                           <Button size="lg" className="bg-white text-{{PRIMARY_COLOR}}-600 hover:bg-gray-100 border-0 shadow-xl">
                               Get Started Now
                           </Button>
                           <Button size="lg" variant="outline" className="text-white border-white hover:bg-white/10 hover:text-white backdrop-blur-sm">
                               Contact Sales
                           </Button>
                       </div>
                   </div>
               </div>
           </div>
        </section>
      </main>
      
      {/* Footer */}
      <footer className="border-t py-12 bg-muted/20">
         <div className="container mx-auto px-4">
            <div className="flex flex-col md:flex-row justify-between items-center gap-6">
               <div className="flex items-center gap-2">
                  <div className="bg-{{PRIMARY_COLOR}}-600 p-1.5 rounded-lg">
                     <Lucide.Boxes className="h-4 w-4 text-white" />
                  </div>
                  <span className="font-bold text-lg">{{BRAND_NAME}}</span>
               </div>
               <div className="text-sm text-muted-foreground">
                  &copy; 2024 {{BRAND_NAME}} Inc. All rights reserved.
               </div>
               <div className="flex gap-4">
                  <Lucide.Twitter className="h-5 w-5 text-muted-foreground hover:text-foreground cursor-pointer transition-colors" />
                  <Lucide.Github className="h-5 w-5 text-muted-foreground hover:text-foreground cursor-pointer transition-colors" />
                  <Lucide.Linkedin className="h-5 w-5 text-muted-foreground hover:text-foreground cursor-pointer transition-colors" />
               </div>
            </div>
         </div>
      </footer>
    </div>
  );
}"""

PRICING_SECTION_SNIPPET = """

        {/* [RYZE_PRICING_SECTION] */}
        <section id="pricing" className="py-24 relative overflow-hidden">
           <div className="container mx-auto px-4">
               <div className="rounded-3xl bg-gradient-to-r from-{{PRIMARY_COLOR}}-600 to-purple-600 p-12 text-center text-white relative overflow-hidden shadow-2xl">
                   <div className="absolute top-0 left-0 w-full h-full bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-overlay"></div>
                   <div className="relative z-10 max-w-2xl mx-auto">
                       <h2 className="text-3xl md:text-4xl font-bold mb-6">Simple, transparent pricing</h2>
                       <p className="text-{{PRIMARY_COLOR}}-100 text-lg mb-8">Choose the plan that fits your team and scale with {{BRAND_NAME}}.</p>
                       <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
                          <Card className="bg-white/10 border-white/20 text-left">
                             <h3 className="text-lg font-semibold mb-2">Starter</h3>
                             <p className="text-sm text-{{PRIMARY_COLOR}}-100 mb-4">Perfect for small projects and prototypes.</p>
                             <p className="text-2xl font-bold mb-4">$0<span className="text-sm font-normal text-{{PRIMARY_COLOR}}-100"> /mo</span></p>
                             <Button size="sm" variant="outline" className="w-full text-white border-white hover:bg-white/10">Get Started</Button>
                          </Card>
                          <Card className="bg-white text-{{PRIMARY_COLOR}}-700 shadow-lg">
                             <h3 className="text-lg font-semibold mb-2">Pro</h3>
                             <p className="text-sm text-gray-600 mb-4">For growing teams shipping production workloads.</p>
                             <p className="text-2xl font-bold mb-4">$39<span className="text-sm font-normal text-gray-500"> /mo</span></p>
                             <Button size="sm" className="w-full bg-{{PRIMARY_COLOR}}-600 text-white hover:bg-{{PRIMARY_COLOR}}-700">Start Pro Trial</Button>
                          </Card>
                          <Card className="bg-white/5 border-white/30 text-left">
                             <h3 className="text-lg font-semibold mb-2">Enterprise</h3>
                             <p className="text-sm text-{{PRIMARY_COLOR}}-100 mb-4">Advanced security, SSO, and custom SLAs.</p>
                             <p className="text-2xl font-bold mb-4">Talk to us</p>
                             <Button size="sm" variant="outline" className="w-full text-white border-white hover:bg-white/10">Contact Sales</Button>
                          </Card>
                       </div>
                   </div>
               </div>
           </div>
        </section>
"""

PORTFOLIO_TEMPLATE = """export default function Portfolio() {
  return (
    <div className="min-h-screen bg-background text-foreground font-sans">
      {/* Hero */}
      <section className="py-20 px-6 text-center">
         <div className="w-32 h-32 mx-auto rounded-full bg-{{PRIMARY_COLOR}}-100 dark:bg-{{PRIMARY_COLOR}}-900/30 mb-6 overflow-hidden border-4 border-{{PRIMARY_COLOR}}-500/20">
            <img src="https://i.pravatar.cc/300?u=portfolio" alt="Profile" className="w-full h-full object-cover" />
         </div>
         <h1 className="text-4xl font-bold mb-4">Hello, I'm <span className="text-{{PRIMARY_COLOR}}-600">{{BRAND_NAME}}</span></h1>
         <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
            A creative developer building beautiful functional web experiences.
         </p>
         <div className="flex justify-center gap-4">
            <Button className="bg-{{PRIMARY_COLOR}}-600 text-white hover:bg-{{PRIMARY_COLOR}}-700">View Work</Button>
            <Button variant="outline">Contact Me</Button>
         </div>
      </section>

      {/* Projects Grid */}
      <section className="py-16 px-6 bg-muted/30">
         <div className="max-w-6xl mx-auto">
            <h2 className="text-2xl font-bold mb-10 text-center">Featured Projects</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
               {[1, 2, 3].map((item) => (
                  <Card key={item} className="overflow-hidden hover:shadow-lg transition-all group">
                     <div className="h-48 bg-gray-200 dark:bg-gray-800 relative overflow-hidden">
                        <div className="absolute inset-0 bg-{{PRIMARY_COLOR}}-500/10 group-hover:bg-{{PRIMARY_COLOR}}-500/0 transition-colors"></div>
                        <div className="flex items-center justify-center h-full text-muted-foreground">Project Preview</div>
                     </div>
                     <div className="p-6">
                        <h3 className="font-bold text-lg mb-2">Project Title {item}</h3>
                        <p className="text-muted-foreground text-sm mb-4">A brief description of this amazing project and the technologies used.</p>
                        <a href="#" className="text-{{PRIMARY_COLOR}}-600 font-medium hover:underline inline-flex items-center gap-1">
                           View Details <Lucide.ArrowRight className="w-3 h-3" />
                        </a>
                     </div>
                  </Card>
               ))}
            </div>
         </div>
      </section>
    </div>
  );
}"""

ECOMMERCE_TEMPLATE = """export default function EcommerceProduct() {
  const [selectedImage, setSelectedImage] = React.useState(0);
  const [quantity, setQuantity] = React.useState(1);

  return (
    <div className="min-h-screen bg-background py-12 px-4 sm:px-6 lg:px-8 font-sans">
      <div className="max-w-7xl mx-auto">
        <div className="lg:grid lg:grid-cols-2 lg:gap-x-8 lg:items-start">
          
          {/* Image Gallery */}
          <div className="flex flex-col-reverse">
            <div className="hidden mt-6 w-full max-w-2xl mx-auto sm:block lg:max-w-none">
              <div className="grid grid-cols-4 gap-6">
                {[0, 1, 2, 3].map((img) => (
                  <button key={img} onClick={() => setSelectedImage(img)} className={`relative h-24 bg-white rounded-md flex items-center justify-center text-sm font-medium uppercase text-gray-900 cursor-pointer hover:bg-gray-50 focus:outline-none focus:ring focus:ring-offset-4 focus:ring-opacity-50 focus:ring-{{PRIMARY_COLOR}}-500 ${selectedImage === img ? 'ring-2 ring-{{PRIMARY_COLOR}}-500' : 'ring-1 ring-gray-200 dark:ring-gray-700'}`}>
                    <span className="sr-only">Image {img + 1}</span>
                    <span className="absolute inset-0 rounded-md overflow-hidden">
                       <div className="w-full h-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-xs text-muted-foreground">Img {img + 1}</div>
                    </span>
                  </button>
                ))}
              </div>
            </div>

            <div className="w-full aspect-w-1 aspect-h-1 rounded-2xl bg-gray-100 dark:bg-gray-800 overflow-hidden border border-border">
               <div className="w-full h-[500px] flex items-center justify-center bg-gray-50 dark:bg-gray-900 relative">
                  <Lucide.ShoppingBag className="w-32 h-32 text-{{PRIMARY_COLOR}}-200 dark:text-{{PRIMARY_COLOR}}-900/50" />
                  <span className="absolute bottom-4 right-4 text-xs text-muted-foreground">Product View {selectedImage + 1}</span>
               </div>
            </div>
          </div>

          {/* Product Info */}
          <div className="mt-10 px-4 sm:px-0 sm:mt-16 lg:mt-0">
            <div className="flex justify-between">
                <h1 className="text-3xl font-extrabold tracking-tight text-foreground">{{BRAND_NAME}} Premium</h1>
                <div className="p-2 bg-{{PRIMARY_COLOR}}-50 dark:bg-{{PRIMARY_COLOR}}-900/20 text-{{PRIMARY_COLOR}}-700 dark:text-{{PRIMARY_COLOR}}-300 rounded-lg text-sm font-bold">New Arrival</div>
            </div>
            
            <div className="mt-3">
              <h2 className="sr-only">Product information</h2>
              <p className="text-3xl text-foreground font-light">$192.00</p>
            </div>

            <div className="mt-3">
               <div className="flex item-center gap-1">
                  {[1,2,3,4,5].map(s => <Lucide.Star key={s} className="w-4 h-4 text-amber-400 fill-amber-400" />)}
                  <span className="text-sm text-muted-foreground ml-2">(148 reviews)</span>
               </div>
            </div>

            <div className="mt-6">
              <h3 className="sr-only">Description</h3>
              <p className="text-base text-muted-foreground space-y-6">
                The {{BRAND_NAME}} Premium is designed for ultimate performance and style. Featuring our proprietary {{PRIMARY_COLOR}} technology, it delivers unmatched results in any environment.
              </p>
            </div>

            <form className="mt-6">
               <div className="flex gap-4 mb-6">
                  <div className="flex-1">
                     <label className="block text-sm font-medium text-muted-foreground mb-1">Quantity</label>
                     <div className="flex items-center border border-border rounded-md">
                        <button type="button" onClick={() => setQuantity(Math.max(1, quantity - 1))} className="p-2 hover:bg-muted"><Lucide.Minus className="w-4 h-4"/></button>
                        <span className="flex-1 text-center font-bold px-4">{quantity}</span>
                        <button type="button" onClick={() => setQuantity(quantity + 1)} className="p-2 hover:bg-muted"><Lucide.Plus className="w-4 h-4"/></button>
                     </div>
                  </div>
                  <div className="flex-1">
                     <label className="block text-sm font-medium text-muted-foreground mb-1">Size</label>
                     <select className="w-full p-2.5 bg-background border border-border rounded-md focus:ring-2 focus:ring-{{PRIMARY_COLOR}}-500">
                        <option>Small</option>
                        <option>Medium</option>
                        <option>Large</option>
                     </select>
                  </div>
               </div>

              <div className="mt-10 flex sm:flex-col1">
                <Button variant="primary" size="lg" className="w-full bg-{{PRIMARY_COLOR}}-600 hover:bg-{{PRIMARY_COLOR}}-700 text-white shadow-xl shadow-{{PRIMARY_COLOR}}-500/20 h-14 text-lg">
                   Add to bag
                </Button>
              </div>
            </form>
            
            <div className="mt-8 border-t border-border pt-8">
               <div className="grid grid-cols-2 gap-4">
                  <div className="flex items-center gap-3 text-sm text-muted-foreground">
                     <Lucide.Truck className="w-5 h-5 text-{{PRIMARY_COLOR}}-600" />
                     <span>Free Shipping</span>
                  </div>
                  <div className="flex items-center gap-3 text-sm text-muted-foreground">
                     <Lucide.ShieldCheck className="w-5 h-5 text-{{PRIMARY_COLOR}}-600" />
                     <span>2 Year Warranty</span>
                  </div>
               </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}"""

GENERIC_TEMPLATE = """export default function GenericPage() {
  const [activeLink, setActiveLink] = React.useState('Home');

  return (
    <div className="min-h-screen bg-background font-sans text-foreground">
      {/* Universal Navbar */}
      <nav className="flex items-center justify-between px-6 py-4 bg-background/80 backdrop-blur-md border-b border-border sticky top-0 z-50">
         <div className="text-xl font-bold flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-{{PRIMARY_COLOR}}-500 to-indigo-600 flex items-center justify-center text-white">
               <Lucide.Zap className="w-5 h-5" />
            </div>
            {{BRAND_NAME}}
         </div>
         <div className="hidden md:flex gap-6">
            {['Home', 'Platform', 'Resources', 'Pricing'].map(link => (
               <button 
                  key={link} 
                  onClick={() => setActiveLink(link)}
                  className={`text-sm font-medium transition-colors ${activeLink === link ? 'text-{{PRIMARY_COLOR}}-600' : 'text-muted-foreground hover:text-foreground'}`}
               >
                  {link}
               </button>
            ))}
         </div>
         <div className="flex gap-2">
            <Button variant="ghost" size="sm">Log In</Button>
            <Button size="sm" className="bg-{{PRIMARY_COLOR}}-600 text-white hover:bg-{{PRIMARY_COLOR}}-700">Get Started</Button>
         </div>
      </nav>

      {/* Main Content Skeleton */}
      <main className="container mx-auto px-4 py-16 space-y-20">
         
         {/* Adaptive Hero */}
         <section className="text-center space-y-6 max-w-4xl mx-auto">
             <div className="inline-flex items-center gap-2 px-3 py-1 bg-{{PRIMARY_COLOR}}-100 dark:bg-{{PRIMARY_COLOR}}-900/30 text-{{PRIMARY_COLOR}}-700 dark:text-{{PRIMARY_COLOR}}-300 rounded-full text-xs font-bold uppercase tracking-wide">
                <span className="w-2 h-2 rounded-full bg-{{PRIMARY_COLOR}}-600 animate-pulse"></span>
                Now Available
             </div>
             <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight">
                Build your next idea with <span className="text-transparent bg-clip-text bg-gradient-to-r from-{{PRIMARY_COLOR}}-600 to-purple-600">{{BRAND_NAME}}</span>
             </h1>
             <p className="text-xl text-muted-foreground leading-relaxed max-w-2xl mx-auto">
                A powerful, scalable, and secure platform designed to help you achieve more. Start building the future today with our advanced tools.
             </p>
             <div className="flex justify-center gap-4 pt-4">
                 <Button size="lg" className="h-12 px-8 bg-{{PRIMARY_COLOR}}-600 hover:bg-{{PRIMARY_COLOR}}-700 text-white shadow-lg shadow-{{PRIMARY_COLOR}}-500/25">Start Free Trial</Button>
                 <Button size="lg" variant="outline" className="h-12 px-8">View Documentation</Button>
             </div>
         </section>

         {/* Content Grid (Generic Features/Items) */}
         <section>
             <div className="flex items-center justify-between mb-8">
                 <h2 className="text-2xl font-bold">Key Capabilities</h2>
                 <Button variant="link" className="text-{{PRIMARY_COLOR}}-600">View All <Lucide.ArrowRight className="w-4 h-4 ml-1"/></Button>
             </div>
             <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                 {[1, 2, 3, 4, 5, 6].map((i) => (
                    <Card key={i} className="hover:border-{{PRIMARY_COLOR}}-500/50 transition-colors cursor-pointer group">
                       <div className="h-32 bg-gray-100 dark:bg-gray-800 rounded-t-xl mb-4 relative overflow-hidden">
                           <div className="absolute inset-0 bg-gradient-to-tr from-{{PRIMARY_COLOR}}-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                           <div className="absolute top-4 left-4 p-2 bg-white dark:bg-black rounded-lg shadow-sm">
                              <Lucide.Layers className="w-5 h-5 text-{{PRIMARY_COLOR}}-600" />
                           </div>
                       </div>
                       <div className="px-6 pb-6 pt-2">
                           <h3 className="font-bold text-lg mb-2">Feature Component {i}</h3>
                           <p className="text-muted-foreground text-sm">A flexible component block that adapts to various content requirements and layouts.</p>
                       </div>
                    </Card>
                 ))}
             </div>
         </section>

         {/* Call to Action Banner */}
         <section className="rounded-3xl bg-gray-900 text-white p-12 overflow-hidden relative">
             <div className="absolute top-0 right-0 w-64 h-64 bg-{{PRIMARY_COLOR}}-500/30 rounded-full blur-[80px] -translate-y-1/2 translate-x-1/2"></div>
             <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-8">
                 <div className="space-y-4">
                     <h2 className="text-3xl font-bold">Ready to get started?</h2>
                     <p className="text-gray-400 max-w-md">Join thousands of others building on {{BRAND_NAME}} platform today.</p>
                 </div>
                 <div className="bg-white p-1 rounded-xl flex">
                     <input type="email" placeholder="Enter your email" className="bg-transparent text-gray-900 px-4 py-2 outline-none w-64" />
                     <Button className="bg-{{PRIMARY_COLOR}}-600 hover:bg-{{PRIMARY_COLOR}}-700 text-white rounded-lg">Subscribe</Button>
                 </div>
             </div>
         </section>

      </main>
      
      {/* Footer */}
      <footer className="border-t py-8 mt-12 bg-muted/20">
         <div className="container mx-auto px-4 text-center text-muted-foreground text-sm">
            &copy; 2024 {{BRAND_NAME}}. All rights reserved.
         </div>
      </footer>
    </div>
  );
}"""

TEMPLATES_MAP = {
    'dashboard': DASHBOARD_TEMPLATE,
    'login': LOGIN_TEMPLATE,
    'form': CONTACT_TEMPLATE,
    'landing': LANDING_TEMPLATE,
    'portfolio': PORTFOLIO_TEMPLATE,
    'ecommerce': ECOMMERCE_TEMPLATE,
    'generic': GENERIC_TEMPLATE
}
