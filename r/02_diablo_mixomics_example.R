# DIABLO mechanics demo using mixOmics (block.splsda)
# Run: Rscript r/02_diablo_mixomics_example.R
# Install: install.packages("mixOmics")

if (!requireNamespace("mixOmics", quietly = TRUE)) {
  stop("Package 'mixOmics' not installed. Run: install.packages('mixOmics')")
}

get_script_dir <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("^--file=", args, value = TRUE)
  script_path <- if (length(file_arg) > 0) sub("^--file=", "", file_arg[1]) else ""
  if (nzchar(script_path)) dirname(normalizePath(script_path)) else getwd()
}

script_dir <- get_script_dir()
repo_root <- normalizePath(file.path(script_dir, ".."))

df <- read.csv(file.path(repo_root, "data", "toy_multiomics_4patients.csv"))

X <- list(
  microbiome = scale(df[, c("BugA", "BugB", "BugC", "BugD")]),
  metabolomics = scale(df[, c("Met1", "Met2", "Met3")]),
  transcriptomics = scale(df[, c("Gene1", "Gene2", "Gene3")])
)

y <- as.factor(df$Group)

# Design matrix controls how much DIABLO encourages correlation across blocks.
# 0 = ignore cross-block correlation; 1 = maximize it.
design <- matrix(
  c(0, 0.1, 0.1,
    0.1, 0, 0.1,
    0.1, 0.1, 0),
  nrow = 3,
  byrow = TRUE
)
colnames(design) <- names(X)
rownames(design) <- names(X)

# keepX selects how many features per block are used in the component.
keepX <- list(microbiome = 2, metabolomics = 2, transcriptomics = 2)

fit <- mixOmics::block.splsda(
  X = X,
  Y = y,
  ncomp = 1,
  keepX = keepX,
  design = design
)

cat("\nDIABLO fit created. With n=4, this is only a mechanics demo.\n")
selected <- mixOmics::selectVar(fit, comp = 1)
print(selected)
