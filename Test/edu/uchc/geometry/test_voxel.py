from unittest import TestCase


class TestVoxel(TestCase):

    def test_interact(self):
        from edu.uchc.geometry.Voxel import Voxel
        from edu.uchc.interactable.Cells import Afumigatus
        from edu.uchc.interactable.Molecules import Iron
        voxel = Voxel(0,0,0)
        voxel.set_agent(Afumigatus(status = Afumigatus.SWELLING_CONIDIA))
        voxel.set_agent(Iron(100))

        for i in range(2):
            if type(voxel.interactables[i]) is Afumigatus:
                print(voxel.interactables[i].boolean_network[Afumigatus.Fe])
            else:
                print(voxel.interactables[i].get())


        voxel.interact()

        for i in range(2):
            if type(voxel.interactables[i]) is Afumigatus:
                print(voxel.interactables[i].boolean_network[Afumigatus.Fe])
            else:
                print(voxel.interactables[i].get())

    def test_update(self):
        from edu.uchc.geometry.Voxel import Voxel
        from edu.uchc.interactable.Cells import Afumigatus
        from edu.uchc.interactable.Molecules import Iron
        voxel = Voxel(0, 0, 0)
        voxel.set_agent(Afumigatus(status=Afumigatus.SWELLING_CONIDIA))
        voxel.set_agent(Iron(100))

        for i in range(2):
            if type(voxel.interactables[i]) is Afumigatus:
                print((voxel.interactables[i].boolean_network[Afumigatus.Fe], voxel.interactables[0 if i == 1 else 1].get()))
            else:
                print(voxel.interactables[i].get())


        for i in range(100):
            voxel.interact()
            voxel.update()

        for i in range(2):
            if type(voxel.interactables[i]) is Afumigatus:
                print((voxel.interactables[i].boolean_network[Afumigatus.Fe], voxel.interactables[0 if i == 1 else 1].get()))
            else:
                print(voxel.interactables[i].get())




