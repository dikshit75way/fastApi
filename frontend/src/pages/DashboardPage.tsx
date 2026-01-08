import { useGetWalletHistoryQuery, useCreatePaymentSessionMutation } from '../features/wallet/walletApi';
import { useGetMeQuery } from '../features/auth/authApi';
import { motion } from 'framer-motion';

export default function DashboardPage() {
    // Force fetch user data on dashboard load to ensure balance is fresh
    const { data: user } = useGetMeQuery(undefined, { pollingInterval: 5000 });
    const { data: transactions, isLoading } = useGetWalletHistoryQuery();
    const [createSession, { isLoading: isPaying }] = useCreatePaymentSessionMutation();

    const handleTopUp = async () => {
        try {
            const res = await createSession({ amount: 1000 }).unwrap(); // $10.00
           console.log(res)
        } catch (err) {
            console.error('Topup failed', err);
        }
    }

    return (
        <div className="container mx-auto p-4 md:p-8">
             <div className="flex flex-col md:flex-row gap-8">
                 {/* Sidebar / Profile Card */}
                 <motion.div 
                    initial={{ x: -20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    className="w-full md:w-1/3 space-y-6"
                 >
                     <div className="bg-card border border-border rounded-xl p-6 shadow-xl">
                         <div className="flex items-center gap-4 mb-6">
                             <div className="w-16 h-16 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500 flex items-center justify-center text-2xl font-bold text-white">
                                 {user?.data?.name?.[0]?.toUpperCase() || 'U'}
                             </div>
                             <div>
                                 <h2 className="text-xl font-bold">{user?.data?.name}</h2>
                                 <p className="text-muted-foreground text-sm">{user?.data?.email}</p>
                                 <span className="inline-block mt-1 px-2 py-0.5 bg-secondary rounded text-xs text-secondary-foreground">{user?.data?.role}</span>
                             </div>
                         </div>
                         
                         <div className="p-4 bg-secondary/30 rounded-lg border border-white/5">
                             <p className="text-sm text-muted-foreground mb-1">Wallet Balance</p>
                             <div className="flex items-center justify-between">
                                 <span className="text-3xl font-bold text-green-400">${user?.data?.wallet_balance || 0}</span>
                                 <button 
                                     onClick={handleTopUp}
                                     disabled={isPaying}
                                     className="px-3 py-1 bg-primary text-primary-foreground text-xs font-bold rounded hover:opacity-90"
                                 >
                                     {isPaying ? 'Processing...' : 'Top Up +$10'}
                                 </button>
                             </div>
                         </div>
                     </div>
                 </motion.div>

                 {/* Main Content / Transactions */}
                 <motion.div 
                    initial={{ x: 20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    className="w-full md:w-2/3"
                 >
                     <h2 className="text-2xl font-bold mb-6">Transaction History</h2>
                     <div className="bg-card border border-border rounded-xl overflow-hidden shadow-sm">
                         {isLoading ? (
                             <div className="p-8 text-center text-muted-foreground">Loading transactions...</div>
                         ) : transactions?.length === 0 ? (
                             <div className="p-8 text-center text-muted-foreground">No transactions found.</div>
                         ) : (
                             <div className="divide-y divide-border">
                                 {transactions?.map((tx) => (
                                     <div key={tx.id} className="p-4 flex items-center justify-between hover:bg-white/5 transition-colors">
                                         <div>
                                             <p className="font-medium text-foreground">{tx.description || tx.transaction_type}</p>
                                             <p className="text-xs text-muted-foreground">{new Date(tx.created_at).toLocaleDateString()}</p>
                                         </div>
                                         <span className={`font-bold ${tx.transaction_type === 'credit' ? 'text-green-400' : 'text-red-400'}`}>
                                             {tx.transaction_type === 'credit' ? '+' : '-'}${tx.amount}
                                         </span>
                                     </div>
                                 ))}
                             </div>
                         )}
                     </div>
                 </motion.div>
             </div>
        </div>
    )
}
