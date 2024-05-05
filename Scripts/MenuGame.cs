using UnityEngine;
using UnityEngine.SceneManagement;


public class MenuGame : MonoBehaviour
{
    public void Easy()
    {
        PlayerPrefs.SetInt("LevelDifficulty", 1);
        SceneManager.LoadScene(2);
    }

    public void Medium()
    {
        PlayerPrefs.SetInt("LevelDifficulty", 2);
        SceneManager.LoadScene(2);
    }

     public void Hard()
    {   
        PlayerPrefs.SetInt("LevelDifficulty", 3);
        SceneManager.LoadScene(2);
    }

   
}
