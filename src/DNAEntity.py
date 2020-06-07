import pygame

from src.Interfaces.GeneCode import GeneCode
from src.Interfaces.RenderObject import RenderObject


class DNAEntity(RenderObject, GeneCode):
    def __init__(self, parent, dna_type: str, r) -> None:
        if dna_type == "worker":
            code = "1"
            name = "dna_" + dna_type
        elif dna_type == "warrior":
            code = "2"
            name = "dna_" + dna_type
        elif dna_type == "queen":
            code = "3"
            name = "dna_" + dna_type
        else:
            code = "J"
            name = "jelly"
        RenderObject.__init__(self, parent=parent)
        GeneCode.__init__(self, code=code)
        self.__image = pygame.image.load("{0}/{1}.png".format(self._res_dir, name)).convert_alpha()
        self.__dna_type = dna_type
        self.resource = r
        self._rect = self.__image.get_rect()

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.__image, self._rect)
