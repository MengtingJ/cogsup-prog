# SET WORKING DIRECTORY FIRST
full_data <- read_csv("data/148338_220209_095045_M057814.csv")
print(full_data)
head(full_data, n=6)
tail(full_data, n=10)
data <- read_csv("data/148338_220209_095045_M057814.csv", skip=2)
print(data)
### Inspecting the dataset
str(data) # Data structure
glimpse(data) # A transposed version of print: columns are rows
summary(data) # An attempt to summarize the information contained in the data
### Data tidying
head(data, 3)
data <- data %>%
  mutate(education = first(response)) %>%
  filter(trialType != "form")

ID <- full_data %>% pull(id) %>% first()
age <- full_data %>% pull(age) %>% first()

data <- data %>% mutate(ID = ID, age = age)

data %>% select(-c(ITI, feedbackTime, `if`:button1))

data %>% 
  select(where(function(col) { n_distinct(col) > 1 }))

data %>% 
  select(where(~ n_distinct(.x) > 1 ), education:age) %>% # Some syntactic sugar (anonymous function) + Keep education level
  select(-c(stimPos_actual, ITI_ms, ITI_f, ITI_fDuration, rowNo)) %>%
  mutate(trial_number = row_number())

(tidy_data <- data %>% 
    select(where(~ n_distinct(.x) > 1), education:age) %>% # Some syntactic sugar (anonimous function) + Keep education level
    select(-c(stimPos_actual, ITI_ms, ITI_f, ITI_fDuration, rowNo)) %>%
    mutate(trial_number = row_number()) %>%
    select(ID, age, education, trial_number, timestamp, trialType, stim1, stim2, stimPos:correct))

data %>% 
  select(where(~ n_distinct(.x) > 1), education:age) %>% # Some syntactic sugar (anonimous function) + Keep education level
  select(-c(stimPos_actual, ITI_ms, ITI_f, ITI_fDuration, rowNo)) %>%
  mutate(trial_number = row_number()) %>%
  select(ID, age, education, trial_number, timestamp, trialType, stim1, stim2, stimPos:correct) %>%
  rename(
    id = ID, trial_type = trialType, 
    stim_pos = stimPos, stim_left = stim1, stim_right = stim2, 
    correct_key = key, correct_side = correctSide,
    rt = RT
  )

data %>% 
  select(where(~ n_distinct(.x) > 1), education:age) %>% # Some syntactic sugar (anonimous function) + Keep education level
  select(-c(stimPos_actual, ITI_ms, ITI_f, ITI_fDuration, rowNo)) %>%
  mutate(trial_number = row_number()) %>%
  select(ID, age, education, trial_number, timestamp, trialType, stim1, stim2, stimPos:correct) %>%
  rename(
    id = ID, trial_type = trialType, 
    stim_pos = stimPos, stim_left = stim1, stim_right = stim2, 
    correct_key = key, correct_side = correctSide,
    rt = RT
  ) %>% head()

tidy_data <- data %>% 
  transmute(
    id = ID, age, education, 
    trial_number = row_number(),
    timestamp, 
    trial_type = trialType,
    stim_left = stim1,
    stim_right = stim2,
    stim_pos = stimPos,
    response,
    rt = RT
  )

tidy_data %>% head()

# ===== Exercise 1 =====
# Add correct_side, correct_key, correct_response, error
library(tidyverse)
tidy_data <- tidy_data %>%
  mutate(
    correct_side = ifelse(str_detect(stim_left, "Small"), "left", "right"),
    correct_key = ifelse(correct_side == "left", "f", "j"),
    correct_response = (response == correct_key),
    error = 1 - correct_response
  )

# ===== Exercise 2 =====
# Add mean_accuracy and mean_rt per participant
tidy_data <- tidy_data %>%
  group_by(id) %>%
  mutate(
    mean_accuracy = mean(correct_response),
    mean_rt = mean(rt)
  ) %>%
  ungroup()

tidy_data %>%
  group_by(trial_type) %>%
  summarize(accuracy = mean(correct_response), rt = mean(rt))

# ===== Exercise 3 =====
# SNARC-like effect: faster when small image is on left?
tidy_data %>%
  count(correct_side)

left_rt  <- tidy_data %>% filter(correct_side == "left") %>% pull(rt)
right_rt <- tidy_data %>% filter(correct_side == "right") %>% pull(rt)

# check normality
shapiro_left  <- shapiro.test(left_rt)$p.value
shapiro_right <- shapiro.test(right_rt)$p.value

if (shapiro_left > 0.05 & shapiro_right > 0.05) {
  # Normality - independent t-test
  test_result <- t.test(left_rt, right_rt, paired = FALSE, alternative = "less")
  test_type <- "Independent t-test"
} else {
  # Non-normality - Wilcoxon rank-sum test
  test_result <- wilcox.test(left_rt, right_rt, paired = FALSE, alternative = "less")
  test_type <- "Wilcoxon rank-sum test"
}

cat("Test used:", test_type, "\n")
print(test_result)


tidy_data %>%
  group_by(trial_type, stim_pos) %>%
  summarize(
    mean_rt = mean(rt),
    mean_accuracy = mean(correct_response)
  )

# ===== Exercise 4 =====
# Does SNARC-like effect depend on trial type?
anova_result <- aov(rt ~ correct_side * trial_type, data = tidy_data)
summary(anova_result)

# ===== Exercise 5 =====
# Load all CSVs and tidy dataset
raw_data <- list.files(path = 'data', pattern = ".csv$", full.names = TRUE) %>%
  map_dfr(read_csv, col_types = cols(), skip = 2, .id = 'file_id')

tidy_full_data <- raw_data %>%
  group_by(file_id) %>%
  mutate(education = first(response)) %>%
  ungroup() %>%
  filter(trialType != "form") %>%
  select(-c(stimPos_actual, ITI_ms, ITI_f, ITI_fDuration, rowNo)) %>%
  mutate(trial_number = row_number())

# ===== Exercise 6 =====
# Exclude trials with RT <200ms or >1500ms
filtered_trials <- tidy_full_data %>%
  filter(rt >= 200, rt <= 1500)
cat("Excluded trials:", nrow(tidy_full_data) - nrow(filtered_trials), "\n")
cat("Proportion excluded:", (nrow(tidy_full_data) - nrow(filtered_trials))/nrow(tidy_full_data), "\n")

# ===== Exercise 7 =====
# Exclude participants with <93% accuracy
participant_acc <- filtered_trials %>%
  group_by(id) %>%
  summarize(mean_acc = mean(correct_response))
good_ids <- participant_acc %>%
  filter(mean_acc >= 0.93) %>%
  pull(id)
filtered_id <- filtered_trials %>% filter(id %in% good_ids)
cat("Excluded participants:", n_distinct(filtered_trials$id) - length(good_ids), "\n")
cat("Proportion excluded:", (n_distinct(filtered_trials$id) - length(good_ids))/n_distinct(filtered_trials$id), "\n")

# ===== Exercise 8 =====
# Summarize RT and accuracy by trial type
filtered_id %>%
  group_by(trial_type) %>%
  summarize(
    mean_rt = mean(rt),
    mean_accuracy = mean(correct_response)
  )

# ===== Exercise 9 =====
# Stroop effect (incongruent - congruent) per participant
stroop_effect <- filtered_id %>%
  group_by(id, trial_type) %>%
  summarize(mean_rt = mean(rt), .groups = 'drop') %>%
  pivot_wider(names_from = trial_type, values_from = mean_rt) %>%
  mutate(stroop_rt = incongruent - congruent)
stroop_effect

# ===== Exercise 10 =====
# Plot histogram of stroop_rt
hist(stroop_effect$stroop_rt, main = "Stroop RT Distribution", xlab = "RT Difference (incongruent - congruent)")

# ===== Exercise 11 =====
# Pivot longer: effect and stroop_value
full_stroop <- filtered_id %>%
  group_by(id, trial_type) %>%
  summarize(
    rt = mean(rt),
    error = mean(1 - correct_response),
    .groups = 'drop'
  ) %>%
  pivot_wider(names_from = trial_type, values_from = c(rt, error)) %>%
  mutate(
    stroop_rt = rt_incongruent - rt_congruent,
    stroop_error = error_incongruent - error_congruent
  )

long_stroop <- full_stroop %>%
  pivot_longer(cols = c(stroop_rt, stroop_error),
               names_to = "effect",
               values_to = "stroop_value")
long_stroop

# ===== Exercise 12 =====
# Plot correlation between stroop_rt and stroop_error
plot(full_stroop$stroop_rt, full_stroop$stroop_error,
     xlab = "Stroop RT", ylab = "Stroop Error", main = "Correlation Stroop RT vs Error")
cor(full_stroop$stroop_rt, full_stroop$stroop_error)
