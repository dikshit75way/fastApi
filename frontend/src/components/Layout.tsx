import { Outlet, Link } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { type RootState } from '../app/store';
import { logout } from '../features/auth/authSlice';

export default function Layout() {
    const { token } = useSelector((state: RootState) => state.auth);
    const dispatch = useDispatch();

    return (
        <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary selection:text-primary-foreground">
            {/* Navbar */}
            <header className="fixed top-0 w-full z-50 border-b border-white/10 bg-black/50 backdrop-blur-md">
                 <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                     <Link to="/" className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
                         Marketplace
                     </Link>
                     <nav className="flex items-center gap-6">
                         <Link to="/marketplace" className="text-sm font-medium hover:text-primary transition-colors">Marketplace</Link>
                         {token ? (
                             <>
                                 <Link to="/dashboard" className="text-sm font-medium hover:text-primary transition-colors">Dashboard</Link>
                                 <button onClick={() => dispatch(logout())} className="text-sm font-medium hover:text-red-400 transition-colors">
                                     Logout
                                 </button>
                             </>
                         ) : (
                             <>
                                 <Link to="/login" className="text-sm font-medium hover:text-primary transition-colors">Login</Link>
                                 <Link to="/register" className="px-4 py-2 rounded-full bg-primary text-primary-foreground text-sm font-medium hover:opacity-90 transition-opacity">
                                     Get Started
                                 </Link>
                             </>
                         )}
                     </nav>
                 </div>
            </header>
            
            <main className="pt-16">
                <Outlet />
            </main>
        </div>
    )
}
