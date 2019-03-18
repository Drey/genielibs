from genie.ops.base import Base
from genie.ops.base import Context

from genie.libs.parser.nxos.show_vpc import ShowVpc


class Vpc(Base):

    def learn(self):
        self.add_leaf(cmd=ShowVpc,
                      src='[vpc]',
                      dest='info[vpc]')

        self.make()