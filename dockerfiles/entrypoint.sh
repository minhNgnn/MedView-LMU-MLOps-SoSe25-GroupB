# entrypoint.sh
#!/usr/bin/env bash
set -euo pipefail

# Configurable via env-vars (override at docker run time):
ENTITY=${WANDB_ENTITY:-theerdhasara-ludwig-maximilianuniversity-of-munich}  # e.g. your GitHub or W&B username/org
PROJECT=${WANDB_PROJECT:-BrainTumorDetection}                               # must match the project in sweep.yaml
CONFIG=${SWEEP_CONFIG:-ml/sweep.yaml}                                          # path inside container
NUM=${NUM:-1}                                                               # number of agents to run

# 1) Create the sweep and grab its ID
# wandb sweep prints a line like: Run: wandb agent ENTITY/PROJECT/SWEEPID
SWEEP_LINE=$(wandb sweep --project "$PROJECT" "$CONFIG" \
  | tee /tmp/_sweep.log \
  | grep -m1 "Run: wandb agent")
SWEEP_ID=${SWEEP_LINE##*/}

echo "Created sweep ${ENTITY}/${PROJECT}/${SWEEP_ID}"

# 2) Launch up to $NUM agents in parallel
for i in $(seq 1 "$NUM"); do
  echo "Starting agent #$i"
  wandb agent "${ENTITY}/${PROJECT}/${SWEEP_ID}" &
done

wait  # wait for all background agents to finish