import { api } from '../../app/api';

export interface Project {
  id: number;
  title: string;
  description: string;
  price: number;
  image_url?: string; // Assuming we might have images
  owner_id: number;
  created_at: string;
}

export const projectsApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getProjects: builder.query<Project[], void>({
      query: () => '/projects/',
      providesTags: ['Projects'],
    }),
    getProjectById: builder.query<Project, number>({
      query: (id) => `/projects/${id}`,
      providesTags: (_result, _error, id) => [{ type: 'Projects', id }],
    }),
    createProject: builder.mutation<Project, FormData>({
      query: (formData) => ({
        url: '/projects/',
        method: 'POST',
        body: formData,
      }),
      invalidatesTags: ['Projects'],
    }),
    deleteProject: builder.mutation<void, number>({
        query: (id) => ({
            url: `/projects/${id}`,
            method: 'DELETE',
        }),
        invalidatesTags: ['Projects'],
    })
  }),
});

export const { 
    useGetProjectsQuery, 
    useGetProjectByIdQuery, 
    useCreateProjectMutation,
    useDeleteProjectMutation
} = projectsApi;
