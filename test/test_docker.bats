#!/usr/bin/env bats

export BASE_IMAGE="base-test-$(< /dev/urandom tr -dc a-z0-9 | head -c 6)"
export DEV_IMAGE="dev-test-$(< /dev/urandom tr -dc a-z0-9 | head -c 6)"

function setup {
  cd "${BATS_TEST_DIRNAME}" && cd ..

  docker build -t "${BASE_IMAGE}" .
  docker build -t "${DEV_IMAGE}" --build-arg BASE_IMAGE -f Dockerfile.dev .
}

function teardown {
  docker rmi "${DEV_IMAGE}"
  docker rmi "${BASE_IMAGE}"
}

@test 'tests inside Docker are running properly' {
  cd "${BATS_TEST_DIRNAME}" && cd ..

  docker run --rm "${DEV_IMAGE}" pytest 2>&1 > kkk.txt
}
