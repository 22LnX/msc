
library(ggplot2)




ggplot(summary_form, aes(x = Mean_length, y = Diamond_percent)) +
  geom_point(color = 'blue') +
  geom_smooth(method = 'lm', col = 'darkblue') +
  labs(title = "Read Length vs. DIAMOND Percentage",
       x = "Mean Read Length",
       y = "DIAMOND Identified Percentage")


ggplot(summary_form, aes(x = Mean_length, y = Blast_percent)) +
  geom_point(color = 'red') +
  geom_smooth(method = 'lm', col = 'darkred') +
  labs(title = "Read Length vs. BLAST Percentage",
       x = "Mean Read Length",
       y = "BLAST Identified Percentage")


cor_diamond <- cor(summary_form$Mean_length, summary_form$Diamond_percent, method = "pearson")
cor_blast <- cor(summary_form$Mean_length, summary_form$Blast_percent, method = "pearson")

cat("Correlation between read length and DIAMOND percentage:", cor_diamond, "\n")
cat("Correlation between read length and BLAST percentage:", cor_blast, "\n")






model_diamond <- lm(Diamond_percent ~ Mean_length + Mean_quality, data = summary_form)
summary(model_diamond)


model_blast <- lm(Blast_percent ~ Mean_length + Mean_quality, data = summary_form)
summary(model_blast)



summary_form$Length_Category <- cut(summary_form$Mean_length, 
                                    breaks = quantile(summary_form$Mean_length, probs = seq(0, 1, 0.25)),
                                    labels = c("Short", "Medium", "Long", "Very Long"), include.lowest = TRUE)

anova_diamond <- aov(Diamond_percent ~ Length_Category, data = summary_form)
summary(anova_diamond)


anova_blast <- aov(Blast_percent ~ Length_Category, data = summary_form)
summary(anova_blast)



par(mfrow = c(1, 2))  
plot(anova_diamond, 1)  
plot(anova_diamond, 2)  


par(mfrow = c(1, 2))  
plot(anova_blast, 1)  
plot(anova_blast, 2)  


tukey_diamond <- TukeyHSD(anova_diamond)
plot(tukey_diamond)


tukey_blast <- TukeyHSD(anova_blast)
plot(tukey_blast)

install.packages('gplots')


sessionInfo()


library(ggplot2)
dev.off()

ggplot(summary_form, aes(x = Length_Category, y = Diamond_percent)) +
  geom_boxplot() +
  geom_jitter(width = 0.2, color = "blue", alpha = 0.5) +
  theme_minimal() +
  labs(title = "Diamond Percentage by Read Length Category", x = "Read Length Category", y = "Diamond Percentage")

ggplot(summary_form, aes(x = Length_Category, y = Blast_percent)) +
  geom_boxplot() +
  geom_jitter(width = 0.2, color = "red", alpha = 0.5) +
  theme_minimal() +
  labs(title = "BLAST Percentage by Read Length Category", x = "Read Length Category", y = "BLAST Percentage")


interaction.plot(summary_form$Length_Category, summary_form$Diamond_percent, summary_form$Diamond_percent, col = 1:4, legend = TRUE)

interaction.plot(summary_form$Length_Category, summary_form$Blast_percent, summary_form$Blast_percent, col = 1:4, legend = TRUE)

if (!requireNamespace("caret", quietly = TRUE)) {
  install.packages("caret")
}

library(caret)


diamond_model <- lm(Diamond_percent ~ Mean_length + Mean_quality, data = summary_form)
summary(diamond_model)

blast_model <- lm(Blast_percent ~ Mean_length + Mean_quality, data = summary_form)
summary(blast_model)

library(ggplot2)
library(broom)

model_diamond <- lm(Diamond_percent ~ Mean_length + Mean_quality, data = summary_form)
model_blast <- lm(Blast_percent ~ Mean_length + Mean_quality, data = summary_form)


plot(model_diamond, which = 1, main = "Residuals vs Fitted for Diamond")


plot(model_blast, which = 1, main = "Residuals vs Fitted for Blast")

plot(model_diamond, which = 2, main = "Normal Q-Q for Diamond")


plot(model_blast, which = 2, main = "Normal Q-Q for Blast")


tidy_model_diamond <- tidy(model_diamond)
ggplot(tidy_model_diamond, aes(x = estimate, y = term)) +
  geom_point() +
  geom_errorbarh(aes(xmin = estimate - std.error, xmax = estimate + std.error)) +
  ggtitle("Coefficient Plot for Diamond")

tidy_model_blast <- tidy(model_blast)
ggplot(tidy_model_blast, aes(x = estimate, y = term)) +
  geom_point() +
  geom_errorbarh(aes(xmin = estimate - std.error, xmax = estimate + std.error)) +
  ggtitle("Coefficient Plot for Blast")



library(ggplot2)
library(gridExtra)

plot_diamond <- ggplot(summary_form, aes(x = Length_Category, y = Diamond_percent)) +
  geom_boxplot() +
  geom_jitter(width = 0.2, color = "blue", alpha = 0.5) +
  theme_minimal() +
  labs(title = "Diamond Percentage by Read Length Category", x = "Read Length Category", y = "Diamond Percentage")

plot_blast <- ggplot(summary_form, aes(x = Length_Category, y = Blast_percent)) +
  geom_boxplot() +
  geom_jitter(width = 0.2, color = "red", alpha = 0.5) +
  theme_minimal() +
  labs(title = "BLAST Percentage by Read Length Category", x = "Read Length Category", y = "BLAST Percentage")


grid.arrange(plot_diamond, plot_blast, ncol = 2)


summary_form$Quality_Category <- cut(summary_form$Mean_quality, 
                                     breaks = quantile(summary_form$Mean_quality, probs = seq(0, 1, 0.25)),
                                     labels = c("Low", "Medium", "High", "Very High"), include.lowest = TRUE)

anova_diamond_quality <- aov(Diamond_percent ~ Quality_Category, data = summary_form)
summary(anova_diamond_quality)


anova_blast_quality <- aov(Blast_percent ~ Quality_Category, data = summary_form)
summary(anova_blast_quality)

plot_diamond <- ggplot(summary_form, aes(x = Quality_Category, y = Diamond_percent)) +
  geom_boxplot() +
  geom_jitter(width = 0.2, color = "blue", alpha = 0.5) +
  theme_minimal() +
  labs(title = "Diamond Percentage by Quality Category", x = "Quality Category", y = "Diamond Percentage")

plot_blast <- ggplot(summary_form, aes(x = Quality_Category, y = Blast_percent)) +
  geom_boxplot() +
  geom_jitter(width = 0.2, color = "red", alpha = 0.5) +
  theme_minimal() +
  labs(title = "BLAST Percentage by Quality Category", x = "Quality Category", y = "BLAST Percentage")

grid.arrange(plot_diamond, plot_blast, ncol = 2)