library(ggplot2)
library(ggalluvial)
library(dplyr)
library(readr)
library(svglite)

file_path <- "E:/NC0104/0729/mantel_test/Hierarchical_Clustering.csv"
data <- read_csv(file_path)

links <- data %>%
  select(Cities1, Cluster_10, Cities2, CulturalGroups) %>%
  group_by(Cluster_10, CulturalGroups) %>%
  summarise(count = n(), .groups = 'drop')


nodes <- data.frame(name = unique(c(links$Cluster_10, links$CulturalGroups)))


cultural_group_colors <- c("Confucian Asia" = "#af7aa1", "Southern Asia" = "#f28e2c", 
                           "Latin America" = "#76b7b2", "Nordic Europe" = "#9c755f", 
                           "Germanic Europe" = "#edc949", "Latin Europe" = "#e15759", 
                           "Eastern Europe" = "#59a14f", "Anglo" = "#4e79a7", 
                           "Arab" = "#ff9da7", "Sub-Sahara Africa" = "#bab0ab")

links <- links %>%
  mutate(color = cultural_group_colors[CulturalGroups])

sankey_plot <- ggplot(data = links,
                      aes(axis1 = Cluster_10, axis2 = CulturalGroups, y = count, fill = CulturalGroups)) +
  geom_alluvium(aes(fill = CulturalGroups), width = 1/12) +
  geom_stratum(width = 1/12) +
  geom_text(stat = "stratum", aes(label = after_stat(stratum)), size = 0) + 
  scale_fill_manual(values = cultural_group_colors) +
  theme_minimal(base_size = 24) + 
  theme(legend.text = element_text(size = 18),         
        legend.title = element_text(size = 20),        
        legend.key.size = unit(3, "lines"),          
        legend.spacing.x = unit(1, "cm"),            
        legend.spacing.y = unit(1, "cm"),            
        axis.title = element_text(size = 20),          
        axis.text = element_text(size = 16),           
        plot.title = element_text(size = 24, face = "bold"),  
        panel.grid.major = element_blank(),           
        panel.grid.minor = element_blank()) +         
  labs(title = "Sankey Diagram",
       x = "Clusters and Cultural Groups",
       y = "Count")


print(sankey_plot)


output_svg_path <- "E:/NC0104/0729/mantel_test/Sankey_Diagram.svg"
ggsave(filename = output_svg_path, plot = sankey_plot, width = 30, height = 24, units = "in")
