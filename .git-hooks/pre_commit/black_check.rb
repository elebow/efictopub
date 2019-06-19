module Overcommit::Hook::PreCommit
  class BlackCheck < Base
    def run
      system('pipenv run black --check --diff .')

      return :pass if $? == 0

      :fail
    end
  end
end
