#!/usr/bin/env bats

export DOCKER_IMAGE="tracking-test-$(< /dev/urandom tr -dc a-z0-9 | head -c 6)"

function setup {
  cd "${BATS_TEST_DIRNAME}" && cd ..
  docker build -t "${DOCKER_IMAGE}" .
}

function teardown {
  docker rmi "${DOCKER_IMAGE}"
}

@test 'tests inside Docker are running properly' {
  docker run --rm "${DOCKER_IMAGE}" pytest
}
