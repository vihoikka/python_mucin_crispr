# Analyzes results and draws graphs from CRISPR-mucin-simulation (python_mucin_crispr.py)
# Ville Hoikkala 2021

library(ggplot2)
library(patchwork)

dada = read.table("../python_mucin_crispr/crispr_sim.csv", sep=",", header = TRUE)
dada$replicate <- as.factor(dada$replicate)

globalAlpha = 0.4

live_dead <- ggplot(data = dada, aes(x=time, y=living, color = replicate)) +
#  geom_point(alpha = 0.4) +
  geom_line(alpha = globalAlpha) +
  ggtitle("Living") +
  theme(legend.position = "none")

roughs <- ggplot(data = dada, aes(x=time, y=rough, color = replicate)) +
  #  geom_point(alpha = 0.4) +
  #  geom_smooth() +
  geom_line(alpha = globalAlpha) +
  ggtitle("Roughs") +
  theme(legend.position = "none")

spacered <- ggplot(data = dada, aes(x=time, y=spacer, color = replicate)) +
  #  geom_point(alpha = 0.4) +
  #  geom_smooth() +
  geom_line(alpha = globalAlpha) +
  ggtitle("CRISPR") +
  theme(legend.position = "none")


mucined <- ggplot(data = dada, aes(x=time, y=mucin_mode, color = replicate)) +
  #  geom_point(alpha = 0.4) +
  #  geom_smooth() +
  geom_line(alpha = globalAlpha) +
  ggtitle("Mucin mode") +
  theme(legend.position = "none")

globalEnergy <- ggplot(data = dada, aes(x=time, y=global_energy_reserves, color = replicate)) +
  #  geom_point(alpha = 0.4) +
  #  geom_smooth() +
  geom_line(alpha = globalAlpha) +
  ggtitle("Global energy reserves") +
  theme(legend.position = "none")

(live_dead | roughs) / (spacered | mucined) / globalEnergy

all_in_one <- ggplot(data = dada, aes(x=time, y=living, group = replicate)) +
  geom_line(alpha = globalAlpha, color = "red") +
  geom_line(aes(x=time, y=mucin_mode*living), alpha = globalAlpha, color = "black", size = 2) +
  ggtitle("Mucin mode")
 # theme(legend.position = "none")
all_in_one
(live_dead | roughs) / (spacered | mucined) / globalEnergy

