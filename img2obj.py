import os
import vtk

def vizualizar_modelo(nomeObjeto):
    # Le o arquivo.obj
    reader = vtk.vtkOBJReader()
    reader.SetFileName(f"objetos/{nomeObjeto}")
    reader.Update()

    # mapper e ator para o modelo
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # renderiza
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(1, 1, 1)

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # iniciar visualização
    render_window.Render()
    render_window_interactor.Start()

def converter(nome_img, nome_objeto):
    diretorio_modelo = "ailia-models/neural_rendering/tripo_sr/"

    os.system(f"cd {diretorio_modelo}&& python3 tripo_sr.py --savepath ../../../objetos/{nome_objeto}")


def main():
    opcao = int(input("1 -> Converter imagem para objeto 3D\n2 -> Vizualizar um Objeto 3D"))
    if opcao == 1:
        nome_img = input("Nome da imagem: ")
        nome_objeto = input("Nome do objeto: ")
        converter(nome_img,nome_objeto)
        opcao = input("Deseja vizualizar o objeto? (1-Sim/2-Não)")
        if opcao == 1:
            vizualizar_modelo(nome_objeto)
    elif opcao == 2:
        nome_objeto = input("Nome do objeto: ")
        vizualizar_modelo(nome_objeto)

if __name__ == "__main__":
    main()