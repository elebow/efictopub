module Overcommit::Hook::PreCommit
  class RunTests < Base
    def run
      system('./run_tests.sh')

      return :pass if $? == 0

      :fail
    end
  end
end
