Feature: Selcal Decoding
    In order to determine the Selcals being received
    As a user
    I want to decode received audio and extract any Selcal calls from it

    Scenario: Streaming audio
        Given I have a source of streaming audio at <Rate> kpbs
        When I use it as input
        And I request a block of audio samples
        Then I should get audio samples

    Scenario: Audio files
        Given I have recorded audio in file <Name>
        When I use it as input
        And I request a block of audio samples
        Then I should get audio samples

    Scenario: Sample rate
        Given I have a source of audio samples
        When I use it as input
        And I request the sample rate
        Then I should get the sample rate of the audio samples

    Scenario Outline: Tone detection
        Given I have an audio sample containing tone <Designator>
        When I process it
        Then I should detect the tone <Frequency> +/- 0.15%
        Examples: Designators
        | Designator    | Frequency |
        | Alpha         | 312.6     |
        | Bravo         | 346.7     |
        | Charlie       | 384.6     |
        | Delta         | 426.6     |
        | Echo          | 473.2     |
        | Foxtrot       | 524.8     |
        | Golf          | 582.1     |
        | Hotel         | 645.7     |
        | Juliet        | 716.1     |
        | Kilo          | 794.3     |
        | Lima          | 881.0     |
        | Mike          | 977.2     |
        | Papa          | 1083.9    |
        | Quebec        | 1202.3    |
        | Romeo         | 1333.5    |
        | Sierra        | 1479.1    |

    Scenario Outline: Silence detection
        Given I have audio samples containing energy but no tones of <Duration> mS long
        When I process it
        Then I should detect <Silence>
        Examples: Silence
        | Duration | Silence |
        | 50 mS    | No      |
        | 100 mS   | Yes     |
        | 200 mS   | Yes     |
        | 300 mS   | Yes     |
        | 350 mS   | No      |

    Scenario Outline: Tone group
        Given I have at least 850 mS of audio samples
        And I detect at least 100 mS of silence at the end of the samples
        And I detect the same two tones <A> and <B> in more than 50% of the samples preceding the silence
        Then I have detected a Tone group

    Scenario Outline: Selcal
        Given I have detected Tone groups <One> and <Two>
        And Tone group <One> contains tones <A> and <B>
        And Tone group <Two> contains tones <C> and <D>
        And tones <A>, <B>, <C>, <D> are all different
        Then the selcal <A><B>-<C><D> has been detected
