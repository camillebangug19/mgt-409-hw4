import { FormEvent, MouseEvent, ReactNode, useEffect, useState } from "react";
import { Link, NavLink, Route, Routes, useLocation, useNavigate, useParams, useSearchParams } from "react-router-dom";

type Product = {
  product_id: string;
  name: string;
  garment_type: string;
  category: string;
  description: string;
  colors: string;
  search_tags: string;
  price: number;
  image_url?: string;
  sizes?: { size: string; quantity: number }[];
  tone?: string;
};

type AuthUser = {
  id: number;
  name: string;
  email: string;
  first_name: string | null;
  last_name: string | null;
};

type AuthResponse = {
  message?: string;
  detail?: string;
  user?: AuthUser;
};

type ChatProduct = {
  product_id: string;
  name: string;
  price: number;
  description: string;
  image_url: string;
  sizes: { size: string; quantity: number }[];
};

type ChatMessage = {
  role: "assistant" | "user";
  content: string;
  products?: ChatProduct[];
};

type ChatPageContext = {
  path: string;
  product_id: string | null;
};

const formatPrice = (price: number) => `$${price.toFixed(2)}`;
const shortDescription = (description: string) => description.length > 96 ? `${description.slice(0, 96).trimEnd()}…` : description;

async function readAuthResponse(response: Response): Promise<AuthResponse | null> {
  const responseText = await response.text();
  if (!responseText.trim()) return null;

  try {
    return JSON.parse(responseText) as AuthResponse;
  } catch {
    return null;
  }
}

function getStoredUser(): AuthUser | null {
  const storedUser = localStorage.getItem("campus_customs_user");
  if (!storedUser) return null;
  try {
    return JSON.parse(storedUser) as AuthUser;
  } catch {
    localStorage.removeItem("campus_customs_user");
    return null;
  }
}

type ProductCategory = { slug: string; name: string; count: number };

function App() {
  return <SiteShell />;
}

function SiteShell() {
  const location = useLocation();
  const [signedInUser, setSignedInUser] = useState<AuthUser | null>(() => getStoredUser());

  useEffect(() => {
    const syncUser = () => setSignedInUser(getStoredUser());
    window.addEventListener("storage", syncUser);
    window.addEventListener("campus-auth-changed", syncUser);
    return () => {
      window.removeEventListener("storage", syncUser);
      window.removeEventListener("campus-auth-changed", syncUser);
    };
  }, []);

  const signOut = () => {
    localStorage.removeItem("campus_customs_user");
    window.dispatchEvent(new Event("campus-auth-changed"));
  };

  return (
    <div className="site-shell">
      <div className="announcement">Officially licensed Yale merchandise · Made for Bulldog Blue pride</div>
      <header className="site-header">
        <Link className="brand" to="/" aria-label="Campus Customs home">
          <span className="brand-mark">CC</span>
          <span>
            <strong>Campus Customs</strong>
            <small>Bulldog Blue, always</small>
          </span>
        </Link>
        <nav className="main-nav" aria-label="Main navigation">
          <NavLink className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")} end to="/">Home</NavLink>
          <ProductCategoryMenu />
          <NavLink className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")} to="/about">About Us</NavLink>
          {signedInUser && <NavLink className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")} to="/woofs">Your Woofs</NavLink>}
        </nav>
        <div className="header-actions">
          {signedInUser ? <div className="account-greeting"><span>Hello, <strong>{signedInUser.first_name ?? signedInUser.name}</strong></span><small>Shopping as {signedInUser.email}</small><button type="button" onClick={signOut}>Sign out</button></div> : <div className="auth-actions"><Link className="auth-link" to="/login">Log In</Link><Link className="auth-link auth-link-primary" to="/create-account">Join the Pack</Link></div>}
          <Link className="bag-link" to="/products" aria-label="Browse products">
            <span aria-hidden="true">↗</span>
            <span className="bag-label">Shop the collection</span>
          </Link>
        </div>
      </header>
      <main key={location.pathname}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/products" element={<ProductsPage user={signedInUser} />} />
          <Route path="/products/:productId" element={<ProductDetailPage user={signedInUser} />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/create-account" element={<CreateAccountPage />} />
          <Route path="/woofs" element={<YourWoofsPage user={signedInUser} />} />
          <Route path="*" element={<HomePage />} />
        </Routes>
      </main>
      <ChatWidget user={signedInUser} pageContext={{ path: location.pathname, product_id: location.pathname.match(/^\/products\/([^/]+)/)?.[1] ?? null }} />
      <footer className="site-footer">
        <div>
          <span className="footer-kicker">Campus Customs</span>
          <p>For the people who never stop talking about Yale.</p>
        </div>
        <span className="footer-note">Officially licensed merchandise · New Haven, CT</span>
      </footer>
    </div>
  );
}

function ProductCategoryMenu() {
  const [categories, setCategories] = useState<ProductCategory[]>([]);

  useEffect(() => {
    fetch("/api/product-categories")
      .then((response) => response.ok ? response.json() as Promise<ProductCategory[]> : [])
      .then(setCategories)
      .catch(() => setCategories([]));
  }, []);

  return <div className="nav-dropdown">
    <NavLink className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")} to="/products">Products <span className="nav-caret">⌄</span></NavLink>
    <div className="nav-dropdown-menu" aria-label="Product categories">
      <NavLink to="/products">All products</NavLink>
      {categories.map((category) => <NavLink key={category.slug} to={`/products?category=${encodeURIComponent(category.slug)}`}>{category.name} <small>{category.count}</small></NavLink>)}
    </div>
  </div>;
}

function HomePage() {
  const [items, setItems] = useState<Product[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/products")
      .then((response) => {
        if (!response.ok) throw new Error("Campus favorites could not be loaded.");
        return response.json() as Promise<Product[]>;
      })
      .then((products) => setItems(products.slice(0, 3)))
      .catch((requestError: Error) => setError(requestError.message));
  }, []);

  return (
    <>
      <section className="hero page-section">
        <div className="hero-copy">
          <p className="eyebrow">The official Yale collection</p>
          <h1>Repping the Bulldog Blue: Officially Licensed Merchandise</h1>
          <p className="hero-description">
            Find the sweatshirt, tee, or forever gift that says Yale without saying a word.
          </p>
          <div className="hero-actions">
            <Link className="button button-primary" to="/products">Shop products <span>↗</span></Link>
            <Link className="text-link" to="/about">Our story <span>→</span></Link>
          </div>
        </div>
        <CampusIllustration />
      </section>
      <section className="feature-strip page-section">
        <div><span className="feature-number">01</span><strong>Officially licensed</strong><p>Real Yale spirit, made right.</p></div>
        <div><span className="feature-number">02</span><strong>Gifts with meaning</strong><p>For every favorite Bulldog.</p></div>
        <div><span className="feature-number">03</span><strong>Easy to love</strong><p>Thoughtful staples for every day.</p></div>
      </section>
      <section className="home-preview page-section">
        <div className="section-heading">
          <div><p className="eyebrow">Popular around campus</p><h2>Find your new favorite.</h2></div>
          <Link className="text-link" to="/products">View all products <span>→</span></Link>
        </div>
        {error ? <div className="api-message"><strong>The campus shop is taking a lap.</strong><span>{error}</span></div> : items.length > 0 ? <FeaturedProductGallery items={items} /> : <div className="api-message">Loading campus favorites…</div>}
      </section>
    </>
  );
}

function CampusIllustration() {
  return <div className="campus-art" aria-label="A playful illustrated Yale campus with buildings and trees">
    <div className="campus-cloud campus-cloud-one" /><div className="campus-cloud campus-cloud-two" />
    <div className="campus-tower"><span>Y</span></div>
    <div className="campus-library"><span>STERLING</span><i /><i /><i /></div>
    <div className="campus-gate"><span>YALE</span><i /><i /><i /><i /></div>
    <div className="campus-tree campus-tree-left"><i /><b /><b /><b /></div>
    <div className="campus-tree campus-tree-right"><i /><b /><b /><b /></div>
    <div className="campus-lawn" /><span className="campus-caption">A little Bulldog Blue, wherever you are</span>
  </div>;
}

function FeaturedProductGallery({ items }: { items: Product[] }) {
  return <div className="featured-photo-grid">{items.map((product, index) => <Link className={`featured-photo featured-photo-${index + 1}`} key={product.product_id} to={`/products/${product.product_id}`}>
    <img src={product.image_url} alt={product.name} />
    <span className="featured-photo-shade" />
    <span className="featured-photo-copy"><small>{product.garment_type}</small><strong>{product.name}</strong><em>{formatPrice(product.price)}</em></span>
  </Link>)}</div>;
}

type WoofApiItem = { saved: boolean; product: Product };

function useWoofs(user: AuthUser | null) {
  const [savedProducts, setSavedProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(Boolean(user));
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    if (!user) {
      setSavedProducts([]);
      setLoading(false);
      setError("");
      return () => { active = false; };
    }
    setLoading(true);
    fetch(`/api/woofs/${user.id}?email=${encodeURIComponent(user.email)}`)
      .then((response) => {
        if (!response.ok) throw new Error("Your Woofs could not be loaded.");
        return response.json() as Promise<WoofApiItem[]>;
      })
      .then((items) => {
        if (active) {
          setSavedProducts(items.map((item) => item.product));
          setError("");
        }
      })
      .catch((requestError: Error) => {
        if (active) setError(requestError.message);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => { active = false; };
  }, [user]);

  const toggleWoof = async (productId: string) => {
    if (!user) return null;
    setError("");
    try {
      const response = await fetch("/api/woofs", {
        body: JSON.stringify({ user_id: user.id, user_email: user.email, product_id: productId }),
        headers: { "Content-Type": "application/json" },
        method: "POST",
      });
      const body = await response.json() as WoofApiItem & { detail?: string };
      if (!response.ok) throw new Error(body.detail ?? "That Woof could not be updated.");
      setSavedProducts((current) => body.saved ? [...current.filter((item) => item.product_id !== productId), body.product] : current.filter((item) => item.product_id !== productId));
      return body.saved;
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "That Woof could not be updated.");
      return null;
    }
  };

  return { savedProducts, savedIds: savedProducts.map((product) => product.product_id), loading, error, toggleWoof };
}

function WoofButton({ productId, user, saved, onToggle }: { productId: string; user: AuthUser | null; saved: boolean; onToggle: (productId: string) => Promise<boolean | null> }) {
  const navigate = useNavigate();
  const [busy, setBusy] = useState(false);

  const handleClick = async (event: MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    event.stopPropagation();
    if (!user) {
      navigate("/login");
      return;
    }
    setBusy(true);
    await onToggle(productId);
    setBusy(false);
  };

  return <button aria-label={user ? (saved ? "Remove this product from Your Woofs" : "Woof this product") : "Log in to Woof this product"} aria-pressed={saved} className={`woof-button${saved ? " woofed" : ""}`} disabled={busy} onClick={handleClick} title={user ? (saved ? "Remove from Your Woofs" : "Save to Your Woofs") : "Log in to save this product"} type="button">🐾</button>;
}

function ProductsPage({ user }: { user: AuthUser | null }) {
  const [items, setItems] = useState<Product[]>([]);
  const [error, setError] = useState("");
  const [searchParams] = useSearchParams();
  const woofs = useWoofs(user);
  const category = searchParams.get("category");
  const visibleItems = category ? items.filter((item) => item.category === category) : items;
  const categoryLabel = category ? category.replaceAll("-", " ").replace(/\b\w/g, (letter) => letter.toUpperCase()).replace("Sweatshirts Hoodies", "Sweatshirts & Hoodies").replace("Jackets Outerwear", "Jackets & Outerwear") : "";

  useEffect(() => {
    fetch("/api/products")
      .then((response) => {
        if (!response.ok) throw new Error("Products could not be loaded.");
        return response.json() as Promise<Product[]>;
      })
      .then(setItems)
      .catch((requestError: Error) => setError(requestError.message));
  }, []);

  return (
    <section className="page-section inner-page">
      <div className="page-heading"><p className="eyebrow">The collection{category ? ` · ${categoryLabel}` : ""}</p><h1>{category ? `${categoryLabel} for Bulldog Blue.` : "Official Bulldog Blue, your way."}</h1><p>From everyday layers to gifts they’ll keep forever.</p></div>
      {error ? <div className="api-message"><strong>Products are taking a lap.</strong><span>{error} Start the FastAPI server to load the catalogue.</span></div> : items.length === 0 ? <div className="api-message">Loading the catalogue…</div> : visibleItems.length === 0 ? <div className="api-message"><strong>No products in this category yet.</strong><Link className="text-link" to="/products">View all products <span>→</span></Link></div> : <ProductGrid items={visibleItems} user={user} savedIds={woofs.savedIds} onToggleWoof={woofs.toggleWoof} />}
      {woofs.error && <p className="woof-error" role="alert">{woofs.error}</p>}
    </section>
  );
}

function ProductGrid({ items, user, savedIds = [], onToggleWoof }: { items: Product[]; user?: AuthUser | null; savedIds?: string[]; onToggleWoof?: (productId: string) => Promise<boolean | null> }) {
  const canWoof = user !== undefined && onToggleWoof !== undefined;
  return <div className="product-grid">{items.map((product, index) => <div className="product-card" key={product.product_id}>
    <Link className="product-card-link" to={`/products/${product.product_id}`}>
      <div className={`product-art ${product.tone ?? ["ink", "slate", "sky", "fog"][index % 4]}`}>{product.image_url ? <img src={product.image_url} alt={product.name} /> : <span className="product-monogram">Y</span>}<span className="product-type">{product.garment_type}</span></div>
      <div className="product-info"><div><h3>{product.name}</h3><p>{shortDescription(product.description)}</p></div><strong>{formatPrice(product.price)}</strong></div>
    </Link>
    {canWoof && <WoofButton productId={product.product_id} user={user} saved={savedIds.includes(product.product_id)} onToggle={onToggleWoof} />}
  </div>)}</div>;
}

function YourWoofsPage({ user }: { user: AuthUser | null }) {
  const woofs = useWoofs(user);
  if (!user) {
    return <section className="page-section inner-page"><div className="page-heading"><p className="eyebrow">Your saved products</p><h1>Your Woofs</h1><p>Log in to save products and keep your favorites close.</p><Link className="button button-primary" to="/login">Log in to see your Woofs <span>↗</span></Link></div></section>;
  }

  return <section className="page-section inner-page woofs-page">
    <div className="page-heading"><p className="eyebrow">Saved for later</p><h1>Your Woofs</h1><p>Products you have paw-marked for your next Campus Customs visit.</p></div>
    {woofs.error ? <div className="api-message"><strong>Your Woofs are taking a lap.</strong><span>{woofs.error}</span></div> : woofs.loading ? <div className="api-message">Loading your Woofs…</div> : woofs.savedProducts.length === 0 ? <div className="api-message"><strong>No Woofs yet.</strong><span>Tap the pawprint on a product you want to revisit.</span><Link className="text-link" to="/products">Browse products <span>→</span></Link></div> : <ProductGrid items={woofs.savedProducts} user={user} savedIds={woofs.savedIds} onToggleWoof={woofs.toggleWoof} />}
  </section>;
}

function ProductDetailPage({ user }: { user: AuthUser | null }) {
  const { productId } = useParams<{ productId: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [error, setError] = useState("");
  const woofs = useWoofs(user);

  useEffect(() => {
    if (!productId) return;
    setProduct(null);
    setError("");
    fetch(`/api/products/${productId}`)
      .then((response) => {
        if (!response.ok) throw new Error("That product could not be found.");
        return response.json() as Promise<Product>;
      })
      .then(setProduct)
      .catch((requestError: Error) => setError(requestError.message));
  }, [productId]);

  if (error) return <section className="page-section detail-page"><div className="api-message"><strong>We couldn’t find that product.</strong><span>{error}</span><Link className="text-link" to="/products">Back to products <span>→</span></Link></div></section>;
  if (!product) return <section className="page-section detail-page"><div className="api-message">Loading product details…</div></section>;

  return <section className="page-section detail-page">
    <Link className="back-link" to="/products">← Back to products</Link>
    <div className="detail-card">
      <div className="detail-image"><img src={product.image_url} alt={product.name} /></div>
      <div className="detail-copy"><p className="eyebrow">{product.garment_type}</p><div className="detail-title-row"><h1>{product.name}</h1><div className="woof-control"><WoofButton productId={product.product_id} user={user} saved={woofs.savedIds.includes(product.product_id)} onToggle={woofs.toggleWoof} /><span>Woof it to save for next time</span></div></div><strong className="detail-price">{formatPrice(product.price)}</strong><p className="detail-description">{product.description}</p>
        <div className="detail-meta"><div><span className="meta-label">Colors</span><p>{product.colors}</p></div><div><span className="meta-label">Search tags</span><p>{product.search_tags}</p></div></div>
        <div className="stock-block"><span className="meta-label">Sizes & stock</span>{product.sizes && product.sizes.length > 0 ? <ul className="stock-list">{product.sizes.map((size) => <li key={size.size}><span>{size.size}</span><strong className={size.quantity === 0 ? "out-of-stock" : ""}>{size.quantity === 0 ? "Out of stock" : `${size.quantity} in stock`}</strong></li>)}</ul> : <p>Stock information will be available soon.</p>}</div>
        {woofs.error && <p className="woof-error" role="alert">{woofs.error}</p>}
      </div>
    </div>
  </section>;
}

function AboutPage() {
  return <section className="page-section inner-page about-page">
    <div className="page-heading"><p className="eyebrow">Our story</p><h1>Big pride. Better gifts.</h1></div>
    <div className="about-grid">
      <div className="about-poster"><span>Yale</span><strong>BLUE</strong><small>EST. 1701 · NEW HAVEN</small></div>
      <div className="about-copy"><p className="lead">Did you or a loved on go to Yale and you don't ever want to shut up about it? You don't have to! Wear your Bulldog Blue pride through our selection of official merchandise, or find that perfect gift for your favorite Yale student, alumnus, relative, or friend.</p><p>Campus Customs brings the best of Yale spirit into one easy place: classic staples, unexpected finds, and gifts for the people who make your own campus story special.</p><Link className="button button-dark" to="/products">Explore the collection <span>↗</span></Link></div>
    </div>
  </section>;
}

function CreateAccountPage() {
  const [form, setForm] = useState({ firstName: "", lastName: "", email: "", password: "", confirmPassword: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setSuccess("");
    if (form.password !== form.confirmPassword) {
      setError("Passwords must match exactly, including capitalization.");
      return;
    }
    setSubmitting(true);
    try {
      const response = await fetch("/api/auth/register", {
        body: JSON.stringify({ first_name: form.firstName, last_name: form.lastName, email: form.email, password: form.password }),
        headers: { "Content-Type": "application/json" },
        method: "POST",
      });
      const body = await readAuthResponse(response);
      if (!response.ok) throw new Error(body?.detail ?? "We could not create your account.");
      if (!body) throw new Error("We could not create your account because the server returned an invalid response.");
      setSuccess(body.message ?? "Your account has been created.");
      setForm({ firstName: "", lastName: "", email: "", password: "", confirmPassword: "" });
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "We could not create your account.");
    } finally {
      setSubmitting(false);
    }
  };

  return <section className="page-section account-page"><div className="account-card"><p className="eyebrow">Campus Customs account</p><h1>Join the pack.</h1><p>Create an account for easier shopping and saved favorites.</p><form onSubmit={handleSubmit}>
    <div className="form-two-column"><label>First name<input autoComplete="given-name" required type="text" value={form.firstName} onChange={(event) => setForm({ ...form, firstName: event.target.value })} /></label><label>Last name<input autoComplete="family-name" required type="text" value={form.lastName} onChange={(event) => setForm({ ...form, lastName: event.target.value })} /></label></div>
    <label>Email address<input autoComplete="email" pattern="[^@\\s]+@[^@\\s]+\\.[^@\\s]+" required type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} /></label>
    <label>Password<input autoComplete="new-password" required type="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} /></label>
    <label>Confirm password<input autoComplete="new-password" required type="password" value={form.confirmPassword} onChange={(event) => setForm({ ...form, confirmPassword: event.target.value })} /></label>
    {error && <p className="form-message error-message" role="alert">{error}</p>}{success && <p className="form-message success-message" role="status">{success}</p>}
    <button className="button button-primary" disabled={submitting} type="submit">{submitting ? "Creating…" : "Create account"} <span>↗</span></button>
  </form></div></section>;
}

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setSuccess("");
    setSubmitting(true);
    try {
      const response = await fetch("/api/auth/login", {
        body: JSON.stringify({ email, password }),
        headers: { "Content-Type": "application/json" },
        method: "POST",
      });
      const body = await readAuthResponse(response);
      if (!response.ok) throw new Error(body?.detail ?? "We could not sign you in.");
      if (!body?.user) throw new Error("We could not sign you in because the server returned an invalid response.");

      localStorage.setItem("campus_customs_user", JSON.stringify(body.user));
      window.dispatchEvent(new Event("campus-auth-changed"));
      setSuccess(body.message ?? "You’re signed in.");
      setTimeout(() => navigate("/"), 700);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "We could not sign you in.");
    } finally {
      setSubmitting(false);
    }
  };

  return <section className="page-section account-page"><div className="account-card"><p className="eyebrow">Campus Customs account</p><h1>Welcome back.</h1><p>Sign in to keep your favorite Bulldog Blue finds close.</p><form onSubmit={handleSubmit}>
    <label>Email address<input autoComplete="email" inputMode="email" required type="text" value={email} onChange={(event) => setEmail(event.target.value)} /></label>
    <label>Password<input autoComplete="current-password" required type="password" value={password} onChange={(event) => setPassword(event.target.value)} /></label>
    {error && <p className="form-message error-message" role="alert">{error}</p>}{success && <p className="form-message success-message" role="status">{success}</p>}
    <button className="button button-primary" disabled={submitting} type="submit">{submitting ? "Signing in…" : "Log in"} <span>↗</span></button>
  </form></div></section>;
}

function ChatWidget({ user, pageContext }: { user: AuthUser | null; pageContext: ChatPageContext }) {
  const [open, setOpen] = useState(false);
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([{ role: "assistant", content: "Hi! I can help you find Bulldog Blue gear, compare products, and check size stock." }]);

  useEffect(() => {
    let active = true;
    const initialMessage: ChatMessage = { role: "assistant", content: "Hi! I can help you find Bulldog Blue gear, compare products, and check size stock." };
    if (!user) {
      setMessages([initialMessage]);
      return () => { active = false; };
    }
    fetch(`/api/chat/history/${user.id}?email=${encodeURIComponent(user.email)}`)
      .then((response) => {
        if (!response.ok) throw new Error("Chat history unavailable.");
        return response.json() as Promise<ChatMessage[]>;
      })
      .then((history) => {
        if (active) setMessages(history.length > 0 ? history : [initialMessage]);
      })
      .catch(() => {
        if (active) setMessages([initialMessage]);
      });
    return () => { active = false; };
  }, [user]);

  const sendMessage = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const message = draft.trim();
    if (!message || sending) return;
    setDraft("");
    setMessages((current) => [...current, { role: "user", content: message }]);
    setSending(true);
    try {
      const conversation = [...messages, { role: "user" as const, content: message }].slice(-8);
      const response = await fetch("/chat", { body: JSON.stringify({ message, user_id: user?.id ?? null, user_email: user?.email ?? null, page_context: pageContext, conversation }), headers: { "Content-Type": "application/json" }, method: "POST" });
      const body = await response.json() as { reply?: string; products?: ChatProduct[]; detail?: string };
      if (!response.ok) throw new Error(body.detail ?? "The shop assistant is temporarily unavailable.");
      setMessages((current) => [...current, { role: "assistant", content: body.reply ?? "I’m not sure how to help with that yet.", products: body.products }]);
    } catch (requestError) {
      setMessages((current) => [...current, { role: "assistant", content: requestError instanceof Error ? requestError.message : "The shop assistant is temporarily unavailable." }]);
    } finally {
      setSending(false);
    }
  };

  return <div className="chat-widget">
    {open && <div className="chat-panel"><div className="chat-panel-header"><div><span className="chat-status" />Campus Guide</div><button type="button" onClick={() => setOpen(false)} aria-label="Close chat">×</button></div><div className="chat-thread">{messages.map((message, index) => <div className={`chat-message ${message.role}`} key={`${message.role}-${index}`}><span className="chat-avatar">{message.role === "assistant" ? "CC" : "You"}</span><div><p>{message.content}</p>{message.products && message.products.length > 0 && <div className="chat-products">{message.products.map((product) => <Link className="chat-product" key={product.product_id} to={`/products/${product.product_id}`}><img src={product.image_url} alt="" /><span><strong>{product.name}</strong><small className="chat-product-description">{shortDescription(product.description)}</small><small className="chat-product-price">{formatPrice(product.price)}</small></span></Link>)}</div>}</div></div>)}{sending && <div className="chat-message assistant"><span className="chat-avatar">CC</span><p className="chat-thinking">Thinking…</p></div>}</div><form className="chat-input-row" onSubmit={sendMessage}><input aria-label="Chat message" disabled={sending} placeholder="Ask about a product…" value={draft} onChange={(event) => setDraft(event.target.value)} /><button type="submit" disabled={sending || !draft.trim()} aria-label="Send message">↑</button></form><small>Product answers come from the Campus Customs catalogue.</small></div>}
    <button className="chat-toggle" type="button" onClick={() => setOpen((current) => !current)}><span className="chat-bubble" aria-hidden="true">✦</span>{open ? "Close chat" : "Chat with us"}</button>
  </div>;
}

export default App;
