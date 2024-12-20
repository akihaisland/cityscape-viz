if (!requireNamespace("ggplot2", quietly = TRUE)) {
  install.packages("ggplot2")
}
if (!requireNamespace("reshape2", quietly = TRUE)) {
  install.packages("reshape2")
}
library(ggplot2)
library(reshape2)

file_path <- "E:/NC0104/0817/cultural_groups_confusion_matrix.csv"
confusion_matrix <- read.csv(file_path, row.names = 1)

confusion_matrix_long <- melt(as.matrix(confusion_matrix))

confusion_matrix_long$Var2 <- factor(confusion_matrix_long$Var2, levels = rev(levels(confusion_matrix_long$Var2)))

heatmap_plot <- ggplot(data = confusion_matrix_long) +
  geom_tile(aes(x = Var1, y = Var2, fill = value), color = "white") +  
  geom_text(aes(x = Var1, y = Var2, label = value), color = "black", size = 4) +  
  scale_fill_gradient(low = "white", high = "#f3a0d7") +
  coord_fixed() +  
  theme_minimal(base_size = 15) + 
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1),  
        axis.text.y = element_text(size = 10),
        legend.title = element_text(size = 12),
        legend.text = element_text(size = 10)) + 
  labs(title = "Confusion Matrix Heatmap",
       x = "Predicted",
       y = "Actual",
       fill = "Count") +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())

print(heatmap_plot)

output_svg_path <- "E:/NC0104/0817/cultural_groups_confusion_matrix_heatmap.svg"
ggsave(filename = output_svg_path, plot = heatmap_plot, width = 10, height = 8, units = "in")
