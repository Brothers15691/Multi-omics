# Load the toy multi-omics dataset and split into blocks
# Run: Rscript r/01_make_toy_data.R

get_script_dir <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("^--file=", args, value = TRUE)
  script_path <- if (length(file_arg) > 0) sub("^--file=", "", file_arg[1]) else ""
  if (nzchar(script_path)) dirname(normalizePath(script_path)) else getwd()
}

script_dir <- get_script_dir()
repo_root <- normalizePath(file.path(script_dir, ".."))

csv_path <- file.path(repo_root, "data", "toy_multiomics_4patients.csv")
df <- read.csv(csv_path)
print(df)

microbiome <- df[, c("BugA", "BugB", "BugC", "BugD")]
metabolomics <- df[, c("Met1", "Met2", "Met3")]
transcriptomics <- df[, c("Gene1", "Gene2", "Gene3")]

y <- as.factor(df$Group)

cat("\nBlock dims:\n")
cat(sprintf("- microbiome: %s\n", paste(dim(microbiome), collapse = " x ")))
cat(sprintf("- metabolomics: %s\n", paste(dim(metabolomics), collapse = " x ")))
cat(sprintf("- transcriptomics: %s\n", paste(dim(transcriptomics), collapse = " x ")))
cat(sprintf("- y (Group): %s levels\n", length(levels(y))))
