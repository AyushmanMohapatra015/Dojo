# Docker scaffold

Day 1 does not build or run containers. Later Dockerfiles will install repository
dependencies at image build time; workers must run offline, as a non-root user,
with CPU/memory limits and disposable workdirs. Never copy API keys into images
or pass them into containers. Hidden-test restoration is owner-written work.
