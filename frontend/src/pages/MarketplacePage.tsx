import { useGetProjectsQuery } from '../features/projects/projectsApi';
import { motion } from 'framer-motion';

export default function MarketplacePage() {
    const { data: projects, isLoading, error } = useGetProjectsQuery();

    if (isLoading) return <div className="text-center p-8 text-muted-foreground">Loading projects...</div>;
    if (error) return <div className="text-center p-8 text-red-400">Failed to load projects</div>;

    return (
        <div className="container mx-auto p-4 md:p-8">
            <h1 className="text-3xl font-bold mb-8 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                Explore Projects
            </h1>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {projects?.data?.map((project) => (
                    <motion.div 
                        key={project.id}
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="bg-card border border-border rounded-xl overflow-hidden shadow-lg hover:shadow-primary/20 transition-all group"
                    >
                        <div className="h-48 bg-secondary/50 relative overflow-hidden">
                           {project.image_url ? (
                               <img src={project.image_url} alt={project.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"/>
                           ) : (
                               <div className="w-full h-full flex items-center justify-center text-muted-foreground">
                                   No Image
                               </div>
                           )}
                        </div>
                        <div className="p-6">
                            <h3 className="text-xl font-bold mb-2 text-foreground">{project.title}</h3>
                            <p className="text-muted-foreground text-sm line-clamp-2 mb-4">{project.description}</p>
                            <div className="flex items-center justify-between">
                                <span className="text-lg font-bold text-green-400">${project.price}</span>
                                <button className="px-4 py-2 bg-primary text-primary-foreground text-sm font-bold rounded-lg hover:opacity-90">
                                    View Details
                                </button>
                            </div>
                        </div>
                    </motion.div>
                ))}
            </div>
            
            {projects?.length === 0 && (
                <div className="text-center text-muted-foreground py-12">
                    No projects found. Be the first to upload one!
                </div>
            )}
        </div>
    )
}
