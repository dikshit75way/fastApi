import { api } from '../../app/api';

export const authApi = api.injectEndpoints({
  endpoints: (builder) => ({
    login: builder.mutation({
      query: (credentials) => {
        // Prepare Form Data for OAuth2
        const formData = new URLSearchParams();
        formData.append('username', credentials.email);
        formData.append('password', credentials.password);
        
        return {
          url: '/auth/token',
          method: 'POST',
          body: formData,
          headers: {
             'Content-Type': 'application/x-www-form-urlencoded',
          },
        };
      },
      // We can invalidate tags or update state here if needed, 
      // but usually we just return the token and handle it in the component.
    }),
    register: builder.mutation({
      query: (userData) => ({
        url: '/auth/register',
        method: 'POST',
        body: userData,
      }),
    }),
    getMe: builder.query({
      query: () => '/auth/me',
      providesTags: ['User'],
    }),
  }),
});

export const { useLoginMutation, useRegisterMutation, useGetMeQuery } = authApi;
