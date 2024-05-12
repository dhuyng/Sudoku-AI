using UnityEngine;
using UnityEngine.SceneManagement;
public class SidesWB : MonoBehaviour
{
    // Start is called before the first frame update
    public void ChooseWhite()
    {
        PlayerPrefs.SetString("PlayerColor", "White");
        SceneManager.LoadScene(1);  // Hàm này sẽ dẫn đến màn hình chọn độ khó
    }

    public void ChooseBlack()
    {
        PlayerPrefs.SetString("PlayerColor", "Black");
        SceneManager.LoadScene(1);
    }
}
