import { api } from '../../app/api';

export interface Transaction {
  id: number;
  amount: number;
  transaction_type: string;
  description: string;
  created_at: string;
}

export interface WalletBalance {
    balance: number;
}

export const walletApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getWalletHistory: builder.query<Transaction[], void>({
      query: () => '/wallets/history/',
      providesTags: ['Wallet'],
    }),
    // Assuming we might have a balance endpoint, currently reusing history or user object
    // But checking backend `wallet/controller.py` might be good. 
    // User object has wallet_balance. We can rely on Auth User or refresh it.
    
    // Let's add top-up mutation
    createPaymentSession: builder.mutation<{ session_id: string; checkout_url: string }, { amount: number }>({
        query: (data) => ({
            url: '/wallets/add',
            method: 'POST',
            body: {
                amount: data.amount, // Amount in cents
              
            }
        })
    })
  }),
});

export const { useGetWalletHistoryQuery, useCreatePaymentSessionMutation } = walletApi;
